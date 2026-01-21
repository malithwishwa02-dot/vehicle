"""
Chronos Agentic API
Exposes Method 5 Engine via REST interface.
"""
import os
import uuid
import json
import threading
import asyncio
import logging
from flask import Flask, request, jsonify, send_file
from core.pipeline import ArtifactPipeline
from main_v5 import OrchestratorV5
from config.settings import SETTINGS

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")

# Job Store (In-Memory for now, use Redis in production)
JOBS = {}
PIPELINE = ArtifactPipeline(os.path.join(os.getcwd(), "uploads"))

def run_orchestrator(job_id, identity_data):
    """
    Wrapper to run Async Orchestrator in a thread.
    """
    try:
        logger.info(f"Starting Job {job_id}")
        JOBS[job_id]['status'] = 'RUNNING'
        
        # Initialize Orchestrator
        orchestrator = OrchestratorV5(identity_data)
        
        # Run Async Lifecycle
        asyncio.run(orchestrator.execute_lifecycle())
        
        JOBS[job_id]['status'] = 'COMPLETED'
        JOBS[job_id]['result'] = orchestrator.profile_path
        
    except Exception as e:
        logger.error(f"Job {job_id} Failed: {e}")
        JOBS[job_id]['status'] = 'FAILED'
        JOBS[job_id]['error'] = str(e)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "version": "5.0.0-AGENTIC"})

@app.route('/generate', methods=['POST'])
def generate_profile():
    """
    Input:
    {
        "proxy": "user:pass@host:port",
        "zip": "10001",
        "age": 90,
        "fullz": {...},
        "config": {...}
    }
    """
    data = request.json
    job_id = str(uuid.uuid4())
    
    # Validate Inputs via Pipeline
    proxy_check = PIPELINE.process_proxy(data.get('proxy', ''))
    if not proxy_check['valid'] and data.get('proxy'):
        return jsonify({"error": f"Invalid Proxy: {proxy_check.get('error')}"}), 400
        
    fullz_check = PIPELINE.process_fullz(data.get('fullz', {}))
    if not fullz_check['valid']:
        return jsonify({"error": f"Invalid Fullz: {fullz_check.get('error')}"}), 400

    # Initialize Job
    JOBS[job_id] = {
        "id": job_id,
        "status": "PENDING",
        "data": data,
        "created_at": str(datetime.now())
    }

    # Start Background Thread
    thread = threading.Thread(target=run_orchestrator, args=(job_id, data))
    thread.start()

    return jsonify({"job_id": job_id, "status": "PENDING"})

@app.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    job = JOBS.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)

@app.route('/export/<job_id>', methods=['GET'])
def export_profile(job_id):
    job = JOBS.get(job_id)
    if not job or job['status'] != 'COMPLETED':
        return jsonify({"error": "Job not ready"}), 400
    
    # Look for mla_export.json
    export_path = os.path.join(job['result'], "mla_export.json")
    if os.path.exists(export_path):
        return send_file(export_path, as_attachment=True)
    
    return jsonify({"error": "Export file not found"}), 500

if __name__ == '__main__':
    from datetime import datetime
    app.run(host='0.0.0.0', port=5000)
