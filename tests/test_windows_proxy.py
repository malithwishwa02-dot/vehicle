import os
import sys
import time
# Ensure project root is importable when pytest executes from a testenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from windows.socks_proxy import start_local_proxy, stop_local_proxy


def test_start_and_stop_proxy():
    server, thread = start_local_proxy(listen_host='127.0.0.1', listen_port=0, upstream_socks=None)
    host, port = server.server_address
    assert port > 0
    # Give the server a moment to start
    time.sleep(0.1)
    stop_local_proxy(server)
    # If shutdown did not raise, test passes
    assert True
