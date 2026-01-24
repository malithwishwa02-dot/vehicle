import json
import os

from LUCID_EMPIRE.core.simulacrum import SimulacrumEngine
from LUCID_EMPIRE import app as lucid_app


def test_genesis_creates_profile(tmp_path):
    pr = tmp_path / "profiles"
    engine = SimulacrumEngine(profile_root=str(pr), dry_run=True)
    opid = "op-test-001"
    fullz = {"name": "Alice", "email": "alice@example.com"}
    res = engine.genesis(opid, fullz, proxy="socks5://127.0.0.1:1080", age_days=30)

    assert res["status"] == "OK"
    path = res["path"]
    assert os.path.isdir(path)
    meta_file = os.path.join(path, "metadata.json")
    assert os.path.isfile(meta_file)

    with open(meta_file, "r", encoding="utf-8") as f:
        meta = json.load(f)
    assert meta["id"] == opid
    assert meta["proxy"] == "socks5://127.0.0.1:1080"


def test_orchestrator_ignite(tmp_path):
    pr = tmp_path / "profiles"
    res = lucid_app.ignite("op-cli-001", "Bob", "bob@example.com", None, profile_root=str(pr), dry_run=True)
    assert res["status"] == "OK"
    assert "config" in res
