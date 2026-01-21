import os, json
from pathlib import Path
root=Path(r"d:\vehicle\37ab1612-c285-4314-b32a-6a06d35d6d84")
inv={}
for p in root.rglob('*'):
    rel=p.relative_to(root)
    key=str(rel)
    try:
        stat=p.stat()
        size=stat.st_size
    except Exception as e:
        size=None
    inv[key]={'is_dir': p.is_dir(), 'size': size}
# For sqlite DBs, try to get table counts
import sqlite3
dbs=['Default/Cookies','Default/History','Default/Login Data','Default/Web Data','Default/Top Sites','first_party_sets.db','first_party_sets.db-journal']
for d in dbs:
    p=root/Path(d)
    if p.exists() and p.is_file():
        try:
            conn=sqlite3.connect(str(p))
            c=conn.cursor()
            counts={}
            for (t,) in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
                try:
                    counts[t]=c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                except Exception as e:
                    counts[t]=str(e)
            inv[str(p.relative_to(root))]['sqlite_tables']=counts
            conn.close()
        except Exception as e:
            inv[str(p.relative_to(root))]['sqlite_error']=str(e)

out= root.parent / 'inventory.json'
with open(out,'w',encoding='utf-8') as fh:
    json.dump(inv, fh, indent=2)
print('Wrote',out)
