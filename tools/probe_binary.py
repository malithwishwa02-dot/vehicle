from pathlib import Path
p=Path(r"d:\vehicle\37ab1612-c285-4314-b32a-6a06d35d6d84\BrowserMetrics-spare.pma")
print('Path:',p)
if not p.exists():
    print('Missing')
else:
    b=p.read_bytes()
    print('Size bytes:',len(b))
    print('First 64 bytes hex:',b[:64].hex())
    s=''
    for c in b[:256]:
        if 32<=c<127:
            s+=chr(c)
        else:
            s+='.'
    print('ASCII-ish preview:',s)
    # find printable strings longer than 6
    import re
    strs=re.findall(b'[ -~]{6,}',b)
    print('Found strings (first 20):')
    for x in strs[:20]:
        try:
            print('-',x.decode('utf-8',errors='ignore'))
        except:
            print('-',x)
