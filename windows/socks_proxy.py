"""Local HTTP(S) proxy that forwards CONNECT (HTTPS) tunnels via an upstream SOCKS5 proxy or direct TCP.

This lightweight proxy is intended to be run locally and pointed to by the browser as an HTTP proxy.
It implements only the CONNECT method (HTTPS tunneling), and forwards the TCP stream to either a
plain TCP connection (direct mode) or to an upstream SOCKS5 proxy (chained mode).

Usage:
    server, thread = start_local_proxy(listen_host='127.0.0.1', listen_port=8080, upstream_socks='socks5://user:pass@host:port')
    # ... when done:
    stop_local_proxy(server)

Note: This is intentionally small and dependency-light. It uses PySocks for upstream SOCKS connections if available.
"""
import socket
import socketserver
import threading
import select
import logging
from urllib.parse import urlparse

try:
    import socks  # PySocks
except Exception:
    socks = None

LOG = logging.getLogger("windows.socks_proxy")
LOG.addHandler(logging.NullHandler())


class _TunnelHandler(socketserver.StreamRequestHandler):
    upstream_socks = None

    def handle(self):
        data = self.rfile.readline().decode('utf-8', errors='ignore')
        if not data:
            return
        parts = data.split()
        if len(parts) < 3:
            return
        method, target, _ = parts
        if method.upper() != 'CONNECT':
            # For simplicity we don't implement full HTTP proxy GET/POST handling.
            self.send_error(405, b'Method Not Allowed')
            return
        host_port = target.split(':')
        host = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 443
        LOG.info(f"CONNECT request to {host}:{port}")

        # Establish outbound connection: either direct socket or via upstream SOCKS
        try:
            if self.upstream_socks:
                if not socks:
                    LOG.error("PySocks not installed; cannot chain to upstream SOCKS proxy")
                    self.send_error(502, b'Bad Gateway')
                    return
                ups = urlparse(self.upstream_socks)
                proxy_host = ups.hostname
                proxy_port = ups.port
                proxy_user = ups.username
                proxy_pass = ups.password
                ss = socks.socksocket()
                ss.set_proxy(socks.SOCKS5, proxy_host, proxy_port, True, proxy_user, proxy_pass)
                ss.settimeout(10)
                ss.connect((host, port))
                remote = ss
            else:
                remote = socket.create_connection((host, port), timeout=10)
        except Exception as e:
            LOG.error(f"Failed to connect to upstream {host}:{port} -> {e}")
            self.send_error(502, b'Bad Gateway')
            return

        # TCP tunnel established
        self.wfile.write(b"HTTP/1.1 200 Connection established\r\n\r\n")
        self.wfile.flush()

        # Relay bytes between client and remote
        try:
            sockets = [self.connection, remote]
            while True:
                r, _, _ = select.select(sockets, [], [], 60)
                if not r:
                    break
                for s in r:
                    if s is self.connection:
                        data = self.connection.recv(4096)
                        if not data:
                            return
                        remote.sendall(data)
                    else:
                        data = remote.recv(4096)
                        if not data:
                            return
                        self.connection.sendall(data)
        finally:
            try:
                remote.close()
            except Exception:
                pass

    def send_error(self, code, msg):
        self.wfile.write(f"HTTP/1.1 {code} Error\r\nContent-Length: {len(msg)}\r\n\r\n".encode('utf-8'))
        self.wfile.write(msg)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def start_local_proxy(listen_host='127.0.0.1', listen_port=8080, upstream_socks: str = None):
    """Start a local HTTP proxy that forwards CONNECT through an upstream socks proxy (optional).

    Returns (server, thread). If listen_port==0 the OS chooses a free port.
    """
    handler = _TunnelHandler
    handler.upstream_socks = upstream_socks
    server = ThreadedTCPServer((listen_host, listen_port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    addr = server.server_address
    LOG.info(f"Local proxy started on {addr[0]}:{addr[1]} upstream_socks={upstream_socks}")
    return server, thread


def stop_local_proxy(server):
    try:
        server.shutdown()
        server.server_close()
        LOG.info("Local proxy stopped")
    except Exception as e:
        LOG.error(f"Error stopping proxy: {e}")
