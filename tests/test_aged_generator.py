import tempfile
import shutil
from pathlib import Path
import subprocess


def test_generate_aged_profile_creates_files():
    tmp = tempfile.mkdtemp(prefix='aged_profile_test_')
    out = Path(tmp) / 'profile'
    try:
        cmd = ['python', 'reproduce_profile/scripts/generate_aged_profile.py', '--out', str(out), '--age-days', '90', '--seed', '1', '--populate']
        subprocess.check_call(cmd)
        assert (out / 'Default' / 'History').exists()
        assert (out / 'Default' / 'Cookies').exists()
        assert (out / 'Default' / 'Login Data').exists()
        assert (out / 'AGED_PROFILE_README.md').exists()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
