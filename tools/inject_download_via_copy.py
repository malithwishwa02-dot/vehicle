#!/usr/bin/env python3
import shutil
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import uuid, hashlib


def to_webkit(dt_obj):
    from datetime import datetime
    epoch_start = datetime(1601,1,1)
    return int((dt_obj - epoch_start).total_seconds() * 1000000)


def inject_download_copy(history_db_path, order_id, file_name=None, t0=None):
    history = Path(history_db_path)
    if not history.exists():
        raise FileNotFoundError(history_db_path)
    tmp = Path(tempfile.mktemp(suffix='.db'))
    shutil.copy2(history, tmp)

    if t0 is None:
        t0 = datetime.now()
    file_name = file_name or f"invoice_{order_id}.pdf"
    fake_path = f"C:/Users/Admin/Downloads/{file_name}"
    url = f"https://target-site.com/invoice/{order_id}.pdf"
    guid = str(uuid.uuid4())
    h = hashlib.md5(fake_path.encode('utf-8')).digest()
    end_time = to_webkit(t0 + timedelta(seconds=5))

    conn = sqlite3.connect(tmp)
    c = conn.cursor()
    try:
        # Determine schema and construct an insert that matches columns (excluding id)
        c.execute("PRAGMA table_info('downloads')")
        cols = [r[1] for r in c.fetchall() if r[1] != 'id']
        # Prepare a default mapping for common columns
        defaults = {
            'guid': guid,
            'current_path': fake_path,
            'target_path': fake_path,
            'start_time': to_webkit(t0),
            'received_bytes': 123456,
            'total_bytes': 123456,
            'state': 1,
            'danger_type': 0,
            'interrupt_reason': 0,
            'hash': h,
            'end_time': end_time,
            'opened': 0,
            'last_access_time': to_webkit(t0),
            'transient': 0,
            'referrer': '',
            'site_url': url,
            'embedder_download_data': '',
            'tab_url': '',
            'tab_referrer_url': '',
            'http_method': 'GET',
            'by_ext_id': '',
            'by_ext_name': '',
            'by_web_app_id': '',
            'etag': '',
            'last_modified': '',
            'mime_type': 'application/pdf',
            'original_mime_type': 'application/pdf'
        }
        values = [defaults.get(cn, '') for cn in cols]
        placeholders = ','.join(['?'] * len(cols))
        col_list = ','.join(cols)
        sql = f"INSERT INTO downloads ({col_list}) VALUES ({placeholders})"
        c.execute(sql, values)
        conn.commit()
    finally:
        conn.close()

    # backup original
    bak = history.with_suffix('.bak')
    shutil.move(str(history), str(bak))
    shutil.move(str(tmp), str(history))
    print('Injected download via copy; original backed up as', bak)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: inject_download_via_copy.py <history_db> [order_id]')
        sys.exit(1)
    inject_download_copy(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else 'ORD-99283')
