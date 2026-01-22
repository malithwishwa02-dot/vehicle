"""Generate an "aged" Chromium profile from redacted dumps and scaffold.

Produces a profile folder with realistic timestamps and sample data
that mimics an older profile for testing. Usage:

python generate_aged_profile.py --out d:\vehicle\aged_profile_demo --age-days 180 --seed 42

"""
from pathlib import Path
import shutil
import argparse
import sqlite3
import random
from datetime import datetime, timedelta
import os

DUMPS_DIR = Path(__file__).parent.parent / 'dumps'
SCAFFOLD_DIR = Path(__file__).parent.parent / 'recreated_profile'

# Chrome internal time: microseconds since 1601-01-01
EPOCH_START = datetime(1601,1,1)

def chrome_time_for_datetime(dt: datetime) -> int:
    delta = dt - EPOCH_START
    micro = int(delta.total_seconds() * 1_000_000)
    return micro


def age_timestamp(days_ago:int, jitter_seconds:int=3600):
    # return chrome-style timestamp that is `days_ago` old with some jitter
    now = datetime.utcnow()
    dt = now - timedelta(days=days_ago, seconds=random.randint(-jitter_seconds, jitter_seconds))
    return chrome_time_for_datetime(dt)


def copy_scaffold(dst: Path):
    # Copy recreated scaffold or create minimal structure
    if SCAFFOLD_DIR.exists():
        shutil.copytree(SCAFFOLD_DIR, dst, dirs_exist_ok=True)
    else:
        dst.mkdir(parents=True, exist_ok=True)
        (dst / 'Default').mkdir()
    return


def execute_sql_dump(sqlfile: Path, dbpath: Path):
    # Execute the SQL dump file into sqlite DB
    dbpath.parent.mkdir(parents=True, exist_ok=True)
    if dbpath.exists():
        dbpath.unlink()
    conn = sqlite3.connect(str(dbpath))
    sql = sqlfile.read_text(encoding='utf-8')
    conn.executescript(sql)
    conn.commit()
    conn.close()


def populate_history(dbpath: Path, days: int, n_urls:int=50):
    conn = sqlite3.connect(str(dbpath))
    c = conn.cursor()
    # create urls table if missing
    c.execute("""CREATE TABLE IF NOT EXISTS urls(id INTEGER PRIMARY KEY AUTOINCREMENT,url LONGVARCHAR,title LONGVARCHAR,visit_count INTEGER DEFAULT 0 NOT NULL,typed_count INTEGER DEFAULT 0 NOT NULL,last_visit_time INTEGER NOT NULL,hidden INTEGER DEFAULT 0 NOT NULL)""")
    now = datetime.utcnow()
    for i in range(n_urls):
        days_ago = random.randint(0, days)
        ts = age_timestamp(days_ago)
        url = f"https://example{random.randint(1,200)}.com/{random.choice(['','','q','a','p'])}{random.randint(0,999)}"
        title = f"Example {random.randint(1,200)}"
        visits = max(1, int(random.expovariate(1/3)))
        c.execute("INSERT INTO urls(url,title,visit_count,typed_count,last_visit_time,hidden) VALUES (?,?,?,?,?,?)", (url,title,visits,0,ts,0))
    conn.commit()
    conn.close()


def populate_cookies(dbpath: Path, days:int, n_cookies:int=200):
    conn = sqlite3.connect(str(dbpath))
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS cookies(creation_utc INTEGER NOT NULL,host_key TEXT NOT NULL,top_frame_site_key TEXT NOT NULL,name TEXT NOT NULL,value TEXT NOT NULL,encrypted_value BLOB NOT NULL,path TEXT NOT NULL,expires_utc INTEGER NOT NULL,is_secure INTEGER NOT NULL,is_httponly INTEGER NOT NULL,last_access_utc INTEGER NOT NULL,has_expires INTEGER NOT NULL,is_persistent INTEGER NOT NULL,priority INTEGER NOT NULL,samesite INTEGER NOT NULL,source_scheme INTEGER NOT NULL,source_port INTEGER NOT NULL,last_update_utc INTEGER NOT NULL,source_type INTEGER NOT NULL,has_cross_site_ancestor INTEGER NOT NULL)""")
    domains = ['google.com','mail.com','example.com','pubmatic.com','workspace.google.com','doubleclick.net']
    for i in range(n_cookies):
        days_ago = random.randint(0, days)
        creation = age_timestamp(days_ago)
        host = random.choice(domains)
        name = random.choice(['SID','NID','OTZ','APISID','HSID','__utma','session']) + str(random.randint(0,999))
        value = f"val{random.randint(1000,999999)}"
        path = '/'
        expires = chrome_time_for_datetime(datetime.utcnow() + timedelta(days=random.randint(30,365)))
        is_secure = 1
        is_http = 0
        last_access = age_timestamp(random.randint(0, days))
        c.execute("INSERT INTO cookies(creation_utc,host_key,top_frame_site_key,name,value,encrypted_value,path,expires_utc,is_secure,is_httponly,last_access_utc,has_expires,is_persistent,priority,samesite,source_scheme,source_port,last_update_utc,source_type,has_cross_site_ancestor) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (creation, host, host, name, value, b'', path, expires, is_secure, is_http, last_access, 1, 1, 1, 0, 0, 0, last_access, 0, 0))
    conn.commit()
    conn.close()


def populate_logins(dbpath: Path, n_logins:int=5, days:int=365):
    conn = sqlite3.connect(str(dbpath))
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS logins (origin_url VARCHAR NOT NULL, action_url VARCHAR, username_element VARCHAR, username_value VARCHAR, password_element VARCHAR, password_value BLOB, submit_element VARCHAR, signon_realm VARCHAR NOT NULL, date_created INTEGER NOT NULL, blacklisted_by_user INTEGER NOT NULL, scheme INTEGER NOT NULL, password_type INTEGER, times_used INTEGER, form_data BLOB, display_name VARCHAR, icon_url VARCHAR, federation_url VARCHAR, skip_zero_click INTEGER, generation_upload_status INTEGER, possible_username_pairs BLOB, id INTEGER PRIMARY KEY AUTOINCREMENT, date_last_used INTEGER NOT NULL DEFAULT 0, date_password_modified INTEGER NOT NULL DEFAULT 0)""")
    for i in range(n_logins):
        days_ago = random.randint(0, days)
        datec = age_timestamp(days_ago)
        email = f'user{random.randint(1,500)}@example.com'
        origin = f'https://login{random.randint(1,20)}.example.com/'
        realm = origin
        # Fill NOT NULL columns with sensible defaults to avoid integrity errors
        blacklisted = 0
        scheme = 0
        times_used = random.randint(1,5)
        date_last_used = datec
        date_password_modified = datec
        c.execute("INSERT INTO logins (origin_url,action_url,username_element,username_value,password_element,password_value,signon_realm,date_created,blacklisted_by_user,scheme,times_used,date_last_used,date_password_modified) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (origin, origin+'auth', 'user', email, 'pass', b'', realm, datec, blacklisted, scheme, times_used, date_last_used, date_password_modified))
    conn.commit()
    conn.close()


def touch_aged_files(root: Path, days:int):
    # set file mtimes to simulate aging
    now = datetime.now()
    for f in root.rglob('*'):
        if f.is_file():
            delta = timedelta(days=random.randint(days-5, days+5))
            t = (now - delta).timestamp()
            try:
                os.utime(f, (t,t))
            except Exception:
                pass


def create_aged_profile(dst: Path, age_days:int=180, seed:int=42, populate:bool=True):
    random.seed(seed)
    if dst.exists():
        print('Removing existing', dst)
        shutil.rmtree(dst)
    copy_scaffold(dst)

    # populate DBs
    if populate:
        print('Populating DBs from dumps...')
        # execute available dumps
        mapping = {
            'Cookies.sql': dst / 'Default' / 'Cookies',
            'History.sql': dst / 'Default' / 'History',
            'Login_Data.sql': dst / 'Default' / 'Login Data',
            'Web_Data.sql': dst / 'Default' / 'Web Data',
            'Top_Sites.sql': dst / 'Default' / 'Top Sites'
        }
        for name, dbpath in mapping.items():
            f = DUMPS_DIR / name
            if f.exists():
                try:
                    execute_sql_dump(f, dbpath)
                except Exception as e:
                    print('Failed to execute dump', name, e)

    # further populate or augment
    populate_history(dst / 'Default' / 'History', age_days, n_urls=200)
    populate_cookies(dst / 'Default' / 'Cookies', age_days, n_cookies=500)
    populate_logins(dst / 'Default' / 'Login Data', n_logins=10, days=age_days)

    # tweak Local State and Preferences
    local_state = dst / 'Local State'
    try:
        import json
        js = json.loads(local_state.read_text(encoding='utf-8')) if local_state.exists() else {}
        js.setdefault('profile', {})
        js['profile'].setdefault('info_cache', {})
        js['profile']['info_cache']['Default'] = {'name':'Your Mimic'}
        js.setdefault('os_crypt', {})
        js['os_crypt']['encrypted_key'] = 'REDACTED-PLACEHOLDER'
        js['last_active_profiles'] = ['Default']
        local_state.write_text(json.dumps(js, indent=2))
    except Exception:
        pass

    # set file mtimes
    touch_aged_files(dst, age_days)

    # write final summary
    summary = dst / 'AGED_PROFILE_README.md'
    summary.write_text(f"Aged profile generated from template. Age days: {age_days}\nSeed: {seed}\nPopulated: {populate}\n")
    print('Aged profile generated at', dst)
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, help='Output profile path')
    ap.add_argument('--age-days', type=int, default=180)
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--populate', action='store_true', help='Populate DBs from dumps')
    args = ap.parse_args()
    create_aged_profile(Path(args.out), age_days=args.age_days, seed=args.seed, populate=args.populate)

if __name__ == '__main__':
    main()