"""Generate redacted SQL dumps and CSV summaries of profile DBs.

Usage: python generate_redacted_dumps.py --outdir ..

This script reads known Chrome profile DBs in the given profile path
and writes SQL dumps with sensitive fields replaced by placeholders.
It does NOT attempt to decrypt encrypted blobs.
"""
import sqlite3
from pathlib import Path
import argparse
import json

SENSITIVE_COLUMNS = {
    'cookies': ['encrypted_value', 'value'],
    'logins': ['password_value', 'username_value', 'display_name', 'origin_url', 'signon_realm'],
    'login data': ['password_value', 'username_value'],
    'login_data': ['password_value', 'username_value'],
}

DB_FILES = {
    'Cookies': 'Default/Cookies',
    'History': 'Default/History',
    'Login Data': 'Default/Login Data',
    'Web Data': 'Default/Web Data',
    'Top Sites': 'Default/Top Sites',
    'first_party_sets': 'first_party_sets.db'
}

PROFILE_ROOT = Path(r"d:\vehicle\37ab1612-c285-4314-b32a-6a06d35d6d84")


def dump_db(path: Path, out_sql: Path, redact=True):
    conn = sqlite3.connect(str(path))
    c = conn.cursor()
    # write schema
    with open(out_sql, 'w', encoding='utf-8') as fh:
        for name, sql in c.execute("SELECT name, sql FROM sqlite_master WHERE type='table';"):
            if sql is None:
                continue
            fh.write(f"-- TABLE: {name}\n")
            fh.write(sql + ";\n\n")
        # export rows
        for (t,) in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            fh.write(f"-- DATA: {t}\n")
            # fetch rows
            col_info = c.execute(f"PRAGMA table_info('{t}')").fetchall()
            cols = [ci[1] for ci in col_info]
            placeholders = []
            for r in c.execute(f"SELECT * FROM {t} LIMIT 1000;"):
                vals = []
                for col, val in zip(cols, r):
                    lp = col.lower()
                    drop = False
                    if redact:
                        # simple redact rules
                        if t.lower() in SENSITIVE_COLUMNS and col in SENSITIVE_COLUMNS[t.lower()]:
                            vals.append("'REDACTED'")
                            continue
                        if 'password' in lp or 'encrypted' in lp or 'secret' in lp or 'salt' in lp:
                            vals.append("'REDACTED'")
                            continue
                    if val is None:
                        vals.append('NULL')
                    elif isinstance(val, (int, float)):
                        vals.append(str(val))
                    else:
                        s = str(val).replace("'", "''")
                        vals.append(f"'{s}'")
                fh.write(f"INSERT INTO {t} ({', '.join(cols)}) VALUES ({', '.join(vals)});\n")
            fh.write('\n')
    conn.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--outdir', default=str(Path(__file__).parent.parent / 'dumps'))
    ap.add_argument('--profile', default=str(PROFILE_ROOT))
    ap.add_argument('--no-redact', action='store_true')
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    profile = Path(args.profile)

    for name, rel in DB_FILES.items():
        p = profile / Path(rel)
        if p.exists():
            target = outdir / (name.replace(' ', '_') + '.sql')
            print('Dumping', p, '->', target)
            dump_db(p, target, redact=not args.no_redact)
        else:
            print('Missing', p)

    # create simple summary JSON
    summary = {}
    for name, rel in DB_FILES.items():
        p = profile / Path(rel)
        if p.exists():
            try:
                conn = sqlite3.connect(str(p))
                c = conn.cursor()
                tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table';")]
                counts = {}
                for t in tables:
                    try:
                        counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                    except Exception as e:
                        counts[t] = str(e)
                summary[name] = counts
                conn.close()
            except Exception as e:
                summary[name] = str(e)
    with open(outdir / 'summary.json', 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2)
    print('Dumps written to', outdir)
