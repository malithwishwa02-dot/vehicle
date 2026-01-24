from pathlib import Path
from LUCID_EMPIRE.core.bootstrap import verify_environment


def test_verify_environment_returns_bool():
    assert isinstance(verify_environment(), bool)
