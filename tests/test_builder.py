import subprocess
import sys


def test_builder_dry_run():
    # Run the builder in dry-run mode
    p = subprocess.run([sys.executable, "builder.py", "--dry-run"], capture_output=True, text=True)
    assert p.returncode == 0
    out = p.stdout + p.stderr
    assert "dry" in out.lower() or "would" in out.lower() or "dry-run" in out.lower()
