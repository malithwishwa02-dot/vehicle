# CHRONOS v4.0 - Hermetic Vehicle

This project builds a hermetic VNC+Browser container with libfaketime-based temporal control.

Quickstart
1. Copy `.env.example` to `.env` and set `CHRONOS_TOKEN` and `PROXY_SOCKS5` if required.
2. Build and start:
   docker-compose up -d --build
3. Connect to VNC: `https://<VPS_IP>:6901` (User: `kasm_user` / Pass: `password123`).
4. Use `http://localhost:5000` inside the VNC to control the internal time.

Security Notes
- Always use a **static residential SOCKS5** proxy for browser traffic.
- Protect port 5000: if exposed, use firewall rules or a reverse proxy with TLS and Basic Auth.
- Do not manually alter the browser resolution or fonts while performing profile operations.
