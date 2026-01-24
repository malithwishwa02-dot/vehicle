"""Verification script for Operation Rebirth scaffolding.
Performs safe, offline checks: file presence, import, instantiate Simulacrum, and run a dry-run.
"""
import os
import importlib
import logging

logging.basicConfig(level=logging.INFO, format='[REVERIFY] %(message)s')
FAIL = '[FAIL]'
PASS = '[PASS]'


def check_file(path):
    if os.path.exists(path):
        logging.info(f"{PASS} Found: {path}")
        return True
    logging.error(f"{FAIL} Missing: {path}")
    return False


def test_simulacrum():
    """Attempt to import the Simulacrum class; if package import fails, load by path."""
    try:
        # Try package import first
        from LUCID_EMPIRE.core.simulacrum import Simulacrum  # type: ignore
    except Exception:
        # Fallback: import by path since folder contains hyphen
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                'simulacrum', os.path.join(os.getcwd(), 'LUCID-EMPIRE', 'core', 'simulacrum.py')
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore
            Simulacrum = getattr(module, 'Simulacrum')
        except Exception as e:
            logging.error(f"{FAIL} Could not import Simulacrum: {e}")
            return False

    try:
        s = Simulacrum({'name': 'Test User', 'email': 'test@example.com'}, scenario='warmup')
        res = s.run(out_dir='/tmp/simulacrum_sanity')
        logging.info(f"{PASS} Simulacrum dry-run returned: {res}")
        return True
    except Exception as e:
        logging.error(f"{FAIL} Simulacrum test failed: {e}")
        return False


def main():
    print('=== Operation Rebirth Verification ===')
    base = os.path.join(os.getcwd(), 'LUCID-EMPIRE')
    checks = [
        os.path.join(base, 'core', 'simulacrum.py'),
        os.path.join(base, 'app.py'),
        os.path.join(base, 'runtime', 'Dockerfile')
    ]
    ok = True
    for p in checks:
        ok = check_file(p) and ok

    if ok:
        ok = test_simulacrum() and ok

    if ok:
        print('\n[PASS] Rebirth scaffolding verified (dry-run).')
    else:
        print('\n[FAIL] Rebirth verification failed. Check logs above.')


if __name__ == '__main__':
    main()
