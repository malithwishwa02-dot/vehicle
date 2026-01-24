"""Orchestrator API for Simulacrum - minimal, safe Flask app.
Exposes endpoints to run a dry-run of the Simulacrum engine.
"""
from flask import Flask, request, jsonify
import logging
from LUCID_EMPIRE.core import simulacrum as simulacrum_module

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok', 'service': 'Simulacrum Orchestrator'})

@app.route('/run_simulacrum', methods=['POST'])
def run_simulacrum():
    data = request.get_json() or {}
    persona = data.get('persona', {'name': 'John Doe', 'email': 'auto@example.com'})
    scenario = data.get('scenario', 'warmup')
    out = data.get('out', '/tmp/simulacrum_profile')

    s = simulacrum_module.Simulacrum(persona, scenario=scenario)
    res = s.run(out_dir=out)
    return jsonify({'status': 'completed', 'result': res})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
