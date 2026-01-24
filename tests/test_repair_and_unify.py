import subprocess


def test_repair_dry_run():
    p = subprocess.run(["bash", "repair_and_unify.sh", "--dry-run"], capture_output=True, text=True)
    assert p.returncode == 0
    out = p.stdout + p.stderr
    assert "DRY-RUN" in out or "Dry-run" in out or "Would" in out
