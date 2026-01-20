from flask import Flask, jsonify, request, render_template, abort
import datetime
import os
import sys

app = Flask(__name__)
TIME_FILE = "/app/time_control/chronos_clock"
TOKEN = os.environ.get('CHRONOS_TOKEN', '').strip()

def check_token(req):
    header = req.headers.get('X-CHRONOS-TOKEN')
    if not TOKEN:
        app.logger.warning('No CHRONOS_TOKEN set — controller is running in unsecured mode')
        return True
    return header == TOKEN

@app.route('/')
def index():
    try:
        with open(TIME_FILE, 'r') as f: current = f.read().strip()
    except Exception:
        current = "REALTIME"
    masked = TOKEN[:6] + '...' if TOKEN else '(not set)'
    return render_template('panel.html', time=current, token=masked)

@app.route('/api/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/jump', methods=['POST'])
def jump():
    if not check_token(request):
        abort(403)

    days = int(request.json.get('days', 0))
    target = datetime.datetime.now() + datetime.timedelta(days=days)
    formatted = f"@{target.strftime('%Y-%m-%d %H:%M:%S')}"

    with open(TIME_FILE, 'w') as f:
        f.write(formatted)

    return jsonify({"status": "warped", "target": formatted})

if __name__ == '__main__':
    # Prefer waitress in production-like containers
    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000)
    except Exception:
        app.run(host='0.0.0.0', port=5000)
