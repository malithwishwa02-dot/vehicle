import os
import sys
import tempfile
from pathlib import Path
import subprocess


def test_lucid_launcher_check_mode(tmp_path):
    # Create a fake bin structure with RunAsDate.exe & firefox
    base = tmp_path
    bin_dir = base / 'bin'
    firefox_dir = bin_dir / 'firefox'
    firefox_dir.mkdir(parents=True)
    (bin_dir / 'RunAsDate.exe').write_text('')
    (firefox_dir / 'firefox.exe').write_text('')

    # Run the launcher in check mode with modified cwd (so it finds bin/)
    cwd = os.getcwd()
    try:
        project_root = Path(__file__).resolve().parents[1]
        script = str(project_root / 'windows' / 'lucid_launcher.py')
        os.chdir(str(base))
        env = os.environ.copy()
        env['PYTHONPATH'] = str(project_root)
        proc = subprocess.run([sys.executable, script, '--check'], capture_output=True, text=True, env=env)
        assert proc.returncode == 0, f"Check mode failed: {proc.stdout}\n{proc.stderr}"
    finally:
        os.chdir(cwd)
