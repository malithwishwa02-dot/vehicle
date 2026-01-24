"""LUCID EMPIRE Orchestrator

Provides a minimal CLI and optional Flask REST shim to invoke the SimulacrumEngine.
"""
import argparse
import logging
from typing import Optional

from LUCID_EMPIRE.core.simulacrum import SimulacrumEngine

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def ignite(operation_id: str, name: str, email: str, proxy: Optional[str], profile_root: str = "./profiles", dry_run: bool = True):
    engine = SimulacrumEngine(profile_root=profile_root, dry_run=dry_run)
    fullz = {"name": name, "email": email}
    return engine.genesis(operation_id, fullz, proxy)


def main():
    parser = argparse.ArgumentParser(prog="lucid-orchestrator")
    parser.add_argument("operation_id", help="Operation identifier")
    parser.add_argument("--name", default="Test User")
    parser.add_argument("--email", default="test@example.com")
    parser.add_argument("--proxy", default=None)
    parser.add_argument("--profile-root", default="./profiles")
    parser.add_argument("--no-dry-run", action="store_true", help="Disable dry run (dangerous)")
    args = parser.parse_args()

    dry_run = not args.no_dry_run
    res = ignite(args.operation_id, args.name, args.email, args.proxy, profile_root=args.profile_root, dry_run=dry_run)
    print(res)


if __name__ == "__main__":
    main()
