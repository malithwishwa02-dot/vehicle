# CHRONOS VEHICLE (v3.2)

Hermetic research station container with integrated KasmVNC + Temporal Controller.

Quickstart
1. Copy `.env.example` to `.env` and set `CHRONOS_TOKEN` and `PROXY_SOCKS5`.
2. Build and start:
   docker-compose up -d --build
3. Connect to VNC: `https://<VPS_IP>:6901` (User: `kasm_user` / Pass: `password123`).
4. Open the browser inside the VNC and use `http://localhost:5000` to control time.

Security Notes
- Always use a **static residential SOCKS5** proxy for browser traffic.
- If you expose port 5000 to the public, restrict it with firewall rules and keep `CHRONOS_TOKEN` secret.
- Do not change the pre-configured resolution or fonts inside the running browser.

Operational Protocol
- Follow the Genesis / Warmup / Sync workflow described in the project documentation.
