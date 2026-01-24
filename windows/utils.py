import os
import logging

logger = logging.getLogger("windows.utils")
logger.addHandler(logging.NullHandler())


def write_firefox_proxy_prefs(profile_path, proxy_host='127.0.0.1', proxy_port=8080):
    """Write a minimal `user.js` to the Firefox profile to force use of the local proxy."""
    try:
        user_js_path = os.path.join(profile_path, 'user.js')
        lines = [
            'user_pref("network.proxy.type", 1);',
            f'user_pref("network.proxy.http", "{proxy_host}");',
            f'user_pref("network.proxy.http_port", {proxy_port});',
            f'user_pref("network.proxy.ssl", "{proxy_host}");',
            f'user_pref("network.proxy.ssl_port", {proxy_port});',
            f'user_pref("network.proxy.socks", "{proxy_host}");',
            f'user_pref("network.proxy.socks_port", {proxy_port});',
            'user_pref("network.proxy.socks_version", 5);',
            'user_pref("network.proxy.allow_hijacking_localhost", true);'
        ]
        os.makedirs(os.path.dirname(user_js_path), exist_ok=True)
        with open(user_js_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        logger.info(f"Wrote proxy prefs to {user_js_path}")
        return True
    except Exception as e:
        logger.warning(f"Failed to write user.js proxy prefs: {e}")
        return False
