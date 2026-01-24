"""LUCID EMPIRE Orchestrator (Flask + CLI)

Provides a Flask REST shim and a CLI entrypoint to invoke the SimulacrumEngine.
"""
import argparse
import logging
from typing import Optional
from pathlib import Path

from flask import Flask, request, jsonify, render_template
from LUCID_EMPIRE.core.simulacrum import SimulacrumEngine
from LUCID_EMPIRE.core.bootstrap import verify_environment

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def ignite(operation_id: str, name: str, email: str, proxy: Optional[str], profile_root: str = "./storage/profiles", dry_run: bool = True):
    engine = SimulacrumEngine(profile_root=profile_root, dry_run=dry_run)
    fullz = {"name": name, "email": email}
    return engine.genesis(operation_id, fullz, proxy, age_days=90)


# Flask app (templates located in interface/)
app = Flask(__name__, template_folder=str(Path(__file__).resolve().parents[1] / "interface"))

@app.before_first_request
def _check_env():
    if not verify_environment():
        # In dev mode we continue, but log the issue
        logger.warning("Environment verification failed on startup.")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/ignite', methods=['POST'])
def ignite_route():
    data = request.get_json() or {}
    op_id = data.get('op_id', 'TEST')
    fullz = data.get('fullz', {})
    proxy = data.get('proxy', None)
    age = int(data.get('age', 90))

    res = ignite(op_id, fullz.get('name', 'API'), fullz.get('email', 'api@example.com'), proxy, profile_root=str(Path(__file__).resolve().parents[1] / "storage" / "profiles"), dry_run=False)
    return jsonify(res)


def main():
    parser = argparse.ArgumentParser(prog="lucid-orchestrator")
    parser.add_argument("operation_id", help="Operation identifier")
    parser.add_argument("--name", default="Test User")
    parser.add_argument("--email", default="test@example.com")
    parser.add_argument("--proxy", default=None)
    parser.add_argument("--profile-root", default="./storage/profiles")
    parser.add_argument("--no-dry-run", action="store_true", help="Disable dry run (dangerous)")
    args = parser.parse_args()

    dry_run = not args.no_dry_run
    res = ignite(args.operation_id, args.name, args.email, args.proxy, profile_root=args.profile_root, dry_run=dry_run)
    print(res)


if __name__ == "__main__":
    main()
