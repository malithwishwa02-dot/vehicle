import os
import sys
import subprocess
import logging
import threading
# webview is imported lazily in GUI mode to avoid heavy deps during CI checks
# Flask is imported lazily inside create_app to avoid requiring Flask for --check CI mode
# core imports (import lazily inside create_app to avoid heavy imports during --check)

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO, format='[LUCID-WIN] %(message)s')
logger = logging.getLogger("Launcher")

# Determine paths for EXE vs Script
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    STORAGE_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'LucidEmpire', 'profiles')
    BIN_DIR = os.path.join(BASE_DIR, 'bin')
else:
    BASE_DIR = os.getcwd()
    STORAGE_DIR = os.path.join(BASE_DIR, 'storage', 'profiles')
    BIN_DIR = os.path.join(BASE_DIR, 'bin')

engine = None  # lazily initialized inside create_app()


def create_app():
    """Create and configure the Flask app (lazy import)."""
    from flask import Flask, render_template, jsonify, request
    app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'interface'))

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/api/ignite', methods=['POST'])
    def ignite():
        data = request.json
        logger.info(f"Ignition Request: {data['op_id']}")
            # 1. GENERATE ARTIFACTS
        # Lazily initialize engine to avoid import-time side effects
        from core.simulacrum import SimulacrumEngine
        global engine
        if engine is None:
            engine = SimulacrumEngine(profile_root=STORAGE_DIR)
        result = engine.genesis(
            operation_id=data['op_id'],
            fullz=data['fullz'],
            proxy=data['proxy'],
            age_days=int(data['age'])
        )
        if result['status'] == "FAILED":
            return jsonify(result), 400

        # 2. START LOCAL PROXY (if proxy provided) AND LAUNCH BROWSER WITH TIME TRAVEL (WINDOWS NATIVE)
        try:
            upstream = data.get('proxy')
            local_proxy = None
            local_proxy_port = None
            # Start a local HTTP proxy that tunnels CONNECT via the provided upstream SOCKS5 proxy
            if upstream:
                from windows.socks_proxy import start_local_proxy
                proxy_server, _ = start_local_proxy(listen_host='127.0.0.1', listen_port=0, upstream_socks=upstream)
                local_proxy = proxy_server
                local_proxy_port = proxy_server.server_address[1]
                logger.info(f"Local proxy listening on 127.0.0.1:{local_proxy_port} chaining to {upstream}")
                # Ensure profile prefs point to this local proxy
                try:
                    from windows.utils import write_firefox_proxy_prefs
                    write_firefox_proxy_prefs(result['path'], '127.0.0.1', local_proxy_port)
                except Exception as e:
                    logger.warning(f"Failed to write proxy prefs to profile: {e}")

            launch_native_browser(result['path'], result['config'])
            return jsonify({"status": "LAUNCHED", "mode": "NATIVE_WINDOWS", "local_proxy_port": local_proxy_port})
        except Exception as e:
            logger.error(f"Launch Failed: {e}")
            return jsonify({"status": "ERROR", "msg": str(e)}), 500

    return app


def start_server():
    app = create_app()
    app.run(port=1337, use_reloader=False)

# Proxy preference writing moved to windows.utils to avoid importing heavy GUI deps during tests



def launch_native_browser(profile_path, config):
    """
    The Core Windows Launcher Logic.
    Uses RunAsDate to inject the fake time into the browser process.
    """
    target_date = config['faketime'].split(" ")[0] # Extract YYYY-MM-DD
    target_time = config['faketime'].split(" ")[1] # Extract HH:MM:SS
    # Path to the RunAsDate executable (bundled in the EXE)
    runner_exe = os.path.join(BIN_DIR, "RunAsDate.exe")
    # Detect Camoufox/Firefox Binary path
    browser_exe = os.path.join(BIN_DIR, "firefox", "firefox.exe")

    # Ensure proxies are respected by profile (if present in config)
    if config.get('proxy') and not (os.path.exists(os.path.join(profile_path, 'user.js'))):
        # If a local proxy was started it will be set by the ignite handler; otherwise we try best-effort
        try:
            write_firefox_proxy_prefs(profile_path, '127.0.0.1', int(config.get('local_proxy_port', 8080)))
        except Exception:
            pass

    cmd = [
        runner_exe,
        "/immediate",
        "/movetime",
        f"/date {target_date}",
        f"/time {target_time}",
        f'"{browser_exe}"',
        "-profile", f'"{profile_path}"',
        "-no-remote"
    ]
    command_str = " ".join(cmd)
    logger.info(f"EXECUTING: {command_str}")
    subprocess.Popen(command_str, shell=True)

def start_server():
    app.run(port=1337, use_reloader=False)

def validate_bundle():
    """Validate that required bundled assets are present (RunAsDate and Firefox)."""
    runner_exe = os.path.join(BIN_DIR, "RunAsDate.exe")
    browser_exe = os.path.join(BIN_DIR, "firefox", "firefox.exe")
    missing = []
    if not os.path.exists(runner_exe):
        missing.append(runner_exe)
    if not os.path.exists(browser_exe):
        missing.append(browser_exe)
    if missing:
        logger.error(f"Bundle validation failed, missing: {missing}")
        return False
    logger.info("Bundle validation OK")
    return True


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Lucid Empire Launcher (Windows)')
    parser.add_argument('--check', action='store_true', help='Check bundled assets and exit (CI friendly)')
    args = parser.parse_args()

    if args.check:
        ok = validate_bundle()
        sys.exit(0 if ok else 2)

    # Thread the Flask Server
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    # Import and open the Native Window (makes it look like a real app, not a browser tab)
    try:
        import webview
        webview.create_window('LUCID EMPIRE | MISSION CONTROL', 'http://localhost:1337', width=1200, height=800, background_color='#000000')
        webview.start()
    except Exception as e:
        logger.warning(f"GUI mode unavailable (webview import failed): {e}")
        # Fall back to running without a native window
        t.join(0.1)

