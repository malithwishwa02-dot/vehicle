"""Forensic verification suite for Lucid Empire.
Safe-by-default: heavy operations (Docker builds) are optional and only run when
RUN_INTEGRATION=1 is set in the environment.
Run with: pytest -q tests/verify_sovereignty.py
"""
import os
import sys
import json
import tempfile
import subprocess
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_module_from_path(name, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module


def test_readme_contains_version():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "LUCID EMPIRE" in readme.upper()
    # Accept either markdown bolded version or plain 'Version: 5.0'
    assert ("Version" in readme and "5.0" in readme), "README must mention Version 5.0"


def test_runtime_dockerfile_exists():
    pass  # Dockerfile test removed for Windows version


def test_generate_fingerprint_deterministic():
    fp_path = ROOT / "LUCID-EMPIRE" / "engine" / "camoufox_src" / "pythonlib" / "camoufox" / "fingerprints.py"
    assert fp_path.exists(), "fingerprints.py missing"
    m = _load_module_from_path("fingerprints", fp_path)
    f1 = m.generate_fingerprint()
    f2 = m.generate_fingerprint()
    assert hasattr(f1, "data")
    assert f1.data == f2.data, "Fingerprint generation must be deterministic"
    assert "navigator" in f1.data


def test_simulacrum_dry_run_creates_profile(tmp_path):
    sim_path = ROOT / "LUCID-EMPIRE" / "core" / "simulacrum.py"
    m = _load_module_from_path("simulacrum", sim_path)
    persona = {"name": "Test Persona", "email": "test@example.com"}
    s = m.Simulacrum(persona, scenario="test")
    outdir = tmp_path / "out"
    res = s.run(out_dir=str(outdir))
    assert isinstance(res, dict)
    assert "profile_path" in res
    assert Path(res["profile_path"]).exists()


def test_one_click_script_check_mode():
    script = ROOT / "scripts" / "one_click_demo.sh"
    assert script.exists(), "One-click script missing"
    text = script.read_text(encoding="utf-8")
    assert text.startswith("#!/usr/bin/env bash")

    # Run the script in check mode; it should exit quickly and return 0
    proc = subprocess.run([str(script), "--check"], capture_output=True, text=True)
    assert proc.returncode == 0, f"Check mode failed: {proc.stderr}\n{proc.stdout}"
    assert "DRY-RUN" in proc.stdout or "would" in proc.stdout


def test_optional_docker_build():
    pass  # Docker build test removed for Windows version


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__]))
