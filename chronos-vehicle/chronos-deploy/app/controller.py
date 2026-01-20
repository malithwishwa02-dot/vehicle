from flask import Flask, jsonify, request, render_template
import datetime
import os

app = Flask(__name__)
TIME_FILE = "/app/time_control/chronos_clock"

@app.route('/')
def index():
    try:
        with open(TIME_FILE, 'r') as f: current = f.read().strip()
    except: current = "REALTIME"
    return render_template('panel.html', time=current)

@app.route('/jump', methods=['POST'])
def jump():
    days = int(request.json.get('days', 0))
    # Logic: Offset from NOW
    target = datetime.datetime.now() + datetime.timedelta(days=days)
    
    # '@' sets absolute time for libfaketime
    formatted = f"@{target.strftime('%Y-%m-%d %H:%M:%S')}"
    
    with open(TIME_FILE, 'w') as f:
        f.write(formatted)
        
    return jsonify({"status": "warped", "target": formatted})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)