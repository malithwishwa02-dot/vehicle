import shutil
import tempfile
import os
from pathlib import Path
import subprocess

def test_fabricate_exact_profile_simulation():
    tmp = tempfile.mkdtemp(prefix='fabricate_test_')
    cwd = os.getcwd()
    try:
        # Run fabricator with forced exact UUID and simulation fallback (no Chrome required)
        proc = subprocess.run(['python', 'fabricate_identity.py', '--uuid', '37ab1612-c285-4314-b32a-6a06d35d6d84', '--force'], check=True, capture_output=True, text=True)
        # Find artifact
        base = Path('generated_profiles')
        artifact = None
        for p in base.iterdir():
            if p.name.startswith('37ab1612'):
                artifact = p
                break
        assert artifact is not None
        # Check LevelDB simulated snapshot exists (or leveldb contains keys)
        lvl = artifact / 'Default' / 'Local Storage' / 'leveldb'
        assert lvl.exists()
        sim_json = lvl / 'local_storage_simulated.json'
        assert sim_json.exists() or (lvl / 'local_storage_simulated.txt').exists() or any(True for _ in lvl.iterdir())
        # Validate injected keys in local_storage_simulated.json
        if sim_json.exists():
            import json
            with open(sim_json, 'r', encoding='utf-8') as fjson:
                data = json.load(fjson)
            for k in ["__stripe_mid", "shopify_checkout_token", "completed_checkout", "last_order_id", "autofill_name", "cc_number"]:
                assert k in data, f"{k} missing from local_storage_simulated.json"

        # Check History file exists and has not-zero size and aged mtime
        hist = artifact / 'Default' / 'History'
        assert hist.exists() and hist.stat().st_size > 0
        mtime = hist.stat().st_mtime
        import time
        age_days = 90
        # mtime should be roughly age_days ago (allow margin)
        assert (time.time() - mtime) > ((age_days - 5) * 24 * 3600)
    finally:
        # cleanup
        try:
            shutil.rmtree('generated_profiles')
        except Exception:
            pass
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)
