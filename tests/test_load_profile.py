import json
import tempfile
from pathlib import Path
from load_profile import load_profile


def test_load_profile_runasdate_command(tmp_path):
    # Create fake profile dir
    profile = tmp_path / 'p1'
    profile.mkdir()
    metadata = {'faketime': '2025-10-23 19:04:21'}
    (profile / 'metadata.json').write_text(json.dumps(metadata))

    # Create fake RunAsDate executable
    bin_dir = Path('bin')
    bin_dir.mkdir(exist_ok=True)
    (bin_dir / 'RunAsDate.exe').write_text('')

    res = load_profile(str(profile), proxy_url='socks5://1.2.3.4:1080', launch=False, force_windows=True)
    assert isinstance(res, dict)
    assert res.get('runner') is not None
    assert res.get('runas_cmd') is not None

    # Cleanup
    (bin_dir / 'RunAsDate.exe').unlink()
