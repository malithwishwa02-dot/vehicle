import sqlite3
from pathlib import Path
base=Path(r"d:\vehicle\37ab1612-c285-4314-b32a-6a06d35d6d84\Default")
# Logins
p=base/'Login Data'
if p.exists():
    conn=sqlite3.connect(str(p))
    c=conn.cursor()
    print('\nLogins rows:')
    for r in c.execute('SELECT id, origin_url, username_value, signon_realm, date_created FROM logins'):
        print(r)
    conn.close()

# Cookies: top domains and sample cookies
p2=base/'Cookies'
if p2.exists():
    conn=sqlite3.connect(str(p2))
    c=conn.cursor()
    print('\nTop 10 cookie host_keys by count:')
    for r in c.execute('SELECT host_key, COUNT(*) as c FROM cookies GROUP BY host_key ORDER BY c DESC LIMIT 10'):
        print(r)
    print('\nSample cookies for google.com:')
    for r in c.execute("SELECT name, value, encrypted_value, path, expires_utc, is_secure FROM cookies WHERE host_key LIKE '%google.com' LIMIT 20"):
        print(r)
    conn.close()
