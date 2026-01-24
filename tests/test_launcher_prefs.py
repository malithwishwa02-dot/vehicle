import tempfile
import os
from windows.utils import write_firefox_proxy_prefs


def test_write_firefox_proxy_prefs(tmp_path):
    profile = tmp_path / 'profile'
    profile.mkdir()
    write_firefox_proxy_prefs(str(profile), '127.0.0.1', 3128)
    user_js = profile / 'user.js'
    assert user_js.exists()
    text = user_js.read_text()
    assert 'network.proxy.type' in text
    assert '127.0.0.1' in text
    assert '3128' in text
