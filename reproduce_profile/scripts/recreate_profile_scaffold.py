"""Create a scaffold of the Chromium profile folder with schema-only DBs and placeholder files.

Usage:
  python recreate_profile_scaffold.py --outdir d:\tmp\mimic_profile --populate-samples

Note: This script creates SQLite DB files with the same tables (and a few sample rows) but does NOT add encrypted secrets.
"""
import sqlite3
from pathlib import Path
import argparse
import json

PROFILE_TEMPLATE = {
    'Last Version': '143.0.7499.41',
    'Last Browser': r'C:\Users\Mimic\mimic_143.3\chrome.exe',
    'MCF': 'cd121410-b711-4e2d-a506-acaf14e198ab',
    'Local State': None,  # written from template below
    'BrowserMetrics-spare.pma': b'\x00' * 4096 * 1  # small placeholder
}

LOCAL_STATE_TEMPLATE = {
    "profile": {"info_cache": {"Default": {"name": "Your Mimic"}}},
    "os_crypt": {"encrypted_key": "REPLACE-WITH-DPAPI-KEY"},
    "last_active_profiles": ["Default"],
    "on_device": {"last_version":"143.0.7499.41"}
}

SQL_SCHEMA_FILES = list(Path(__file__).parent.parent.joinpath('dumps').glob('*.sql'))


def write_text(p: Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')


def write_binary(p: Path, b: bytes):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b)


def create_sqlite_from_schema(sqlfile: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(dest))
    c = conn.cursor()
    with open(sqlfile, 'r', encoding='utf-8') as fh:
        sql = fh.read()
    # Try to execute CREATE TABLE statements
    for stmt in sql.split(';'):
        s = stmt.strip()
        if not s:
            continue
        try:
            c.execute(s)
        except Exception:
            # ignore inserts, keep only CREATE TABLE
            pass
    conn.commit()
    conn.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--outdir', default=str(Path.cwd() / 'recreated_profile'))
    ap.add_argument('--populate-samples', action='store_true')
    args = ap.parse_args()
    out = Path(args.outdir)
    # create files
    for name, content in PROFILE_TEMPLATE.items():
        p = out / name
        if isinstance(content, bytes):
            write_binary(p, content)
        elif content is None:
            if name == 'Local State':
                write_text(p, json.dumps(LOCAL_STATE_TEMPLATE, indent=2))
            else:
                write_text(p, '')
        else:
            write_text(p, str(content))
    # create directories
    dirs = ['ActorSafetyLists', 'AutofillStates', 'BrowserMetrics', 'Crashpad/attachments', 'Crashpad/reports', 'component_crx_cache', 'extensions_crx_cache', 'GraphiteDawnCache', 'GrShaderCache', 'Default']
    for d in dirs:
        (out / d).mkdir(parents=True, exist_ok=True)
    # copy metadata.json placeholders
    for md in ['component_crx_cache/metadata.json', 'extensions_crx_cache/metadata.json']:
        write_text(out / md, json.dumps({"hashes":{}}, indent=2))
    # create Default profile common files
    default = out / 'Default'
    (default).mkdir(exist_ok=True)
    # copy SQL schema files into DBs in Default
    for sqlf in SQL_SCHEMA_FILES:
        dbname = sqlf.stem.replace('_',' ')
        dest = default / dbname
        print('Creating DB', dest)
        create_sqlite_from_schema(sqlf, dest)
    # create Preferences
    write_text(default / 'Preferences', json.dumps({"profile":{"name":"Your Mimic"}, "exit_type":"Crashed"}, indent=2))
    # create README
    readme = out / 'README'
    write_text(readme, 'This is a scaffold of a Chromium profile generated for test purposes.')
    print('Recreated scaffold at', out)
