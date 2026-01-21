"""Decrypt Chromium profile secrets (cookies, saved logins) using Windows DPAPI and Local State AES key.

Outputs:
 - d:\vehicle\reproduce_profile\exports\cookies.csv
 - d:\vehicle\reproduce_profile\exports\logins.csv
 - d:\vehicle\reproduce_profile\exports\autofill.csv
 - d:\vehicle\reproduce_profile\exports\addresses.csv
 - d:\vehicle\reproduce_profile\exports\report.md
 - d:\vehicle\reproduce_profile\exports\raw_files/ (trusted_vault.pb, passkey_enclave_state)

Note: Requires running on the same Windows user account that owns the profile.
"""
import os, json, base64, csv, sqlite3, traceback
from pathlib import Path
from typing import Optional

PROFILE_ROOT = Path(r"d:\vehicle\37ab1612-c285-4314-b32a-6a06d35d6d84")
EXPORT_DIR = Path(r"d:\vehicle\reproduce_profile\exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = EXPORT_DIR / 'raw_files'
RAW_DIR.mkdir(exist_ok=True)

# DPAPI support: try win32crypt, else use ctypes fallback
try:
    import win32crypt
    def dpapi_unprotect(data: bytes) -> bytes:
        return win32crypt.CryptUnprotectData(data, None, None, None, 0)[1]
except Exception:
    import ctypes
    from ctypes import wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', wintypes.DWORD), ('pbData', ctypes.c_void_p)]

    def dpapi_unprotect(data: bytes) -> bytes:
        # Try ctypes CryptUnprotectData first
        try:
            # allocate buffer and set DATA_BLOB fields explicitly
            buf = ctypes.create_string_buffer(data, len(data))
            blob_in = DATA_BLOB()
            blob_in.cbData = len(data)
            blob_in.pbData = ctypes.cast(buf, ctypes.c_void_p)
            blob_out = DATA_BLOB()
            ok = ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out))
            if ok:
                pointer = ctypes.cast(blob_out.pbData, ctypes.POINTER(ctypes.c_ubyte * blob_out.cbData))
                result = bytes(pointer.contents)
                ctypes.windll.kernel32.LocalFree(blob_out.pbData)
                return result
            else:
                # record error code
                err = ctypes.GetLastError()
                errors.append(('dpapi_ctypes_failed', f'CryptUnprotectData returned {err}', ''))
        except Exception as e:
            errors.append(('dpapi_ctypes_exception', str(e), ''))
            pass
        # Fallback: use PowerShell ProtectedData Unprotect
        try:
            import subprocess
            b64 = base64.b64encode(data).decode('ascii')
            pwsh = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
            cmd = [pwsh, '-NoProfile', '-Command', "[System.Convert]::ToBase64String([System.Security.Cryptography.ProtectedData]::Unprotect([System.Convert]::FromBase64String('%s'), $null, [System.Security.Cryptography.DataProtectionScope]::CurrentUser))" % b64]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode == 0:
                out_b64 = proc.stdout.strip()
                return base64.b64decode(out_b64)
            else:
                errors.append(('powershell_dpapi_failed', proc.stderr.strip(), ''))
                raise RuntimeError('PowerShell DPAPI failed: ' + proc.stderr.strip())
        except Exception as e:
            raise e


# AES-GCM
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except Exception as e:
    raise SystemExit('cryptography required; pip install cryptography')

report_lines = []
errors = []

def get_local_state_key(local_state_path: Path) -> Optional[bytes]:
    try:
        j = json.loads(local_state_path.read_text(encoding='utf-8'))
        enc_key_b64 = j['os_crypt']['encrypted_key']
        enc_key = base64.b64decode(enc_key_b64)
        # Chrome on Windows prefixes with 'DPAPI'
        if enc_key.startswith(b'DPAPI'):
            enc_key = enc_key[5:]
        # DPAPI decrypt using dpapi_unprotect
        descr = dpapi_unprotect(enc_key)
        return descr
    except Exception as e:
        errors.append(('local_state_key', str(e), traceback.format_exc()))
        return None

# Decrypt value (cookies or passwords)
def decrypt_value(encrypted_value: bytes, key: Optional[bytes]) -> Optional[str]:
    try:
        if not encrypted_value:
            return ''
        if encrypted_value.startswith(b'v10') or encrypted_value.startswith(b'v11'):
            # AES-GCM: prefix 'v10' then 12-byte nonce then ciphertext+tag
            payload = encrypted_value[3:]
            nonce = payload[:12]
            ct_and_tag = payload[12:]
            aesgcm = AESGCM(key)
            plain = aesgcm.decrypt(nonce, ct_and_tag, None)
            return plain.decode('utf-8', errors='ignore')
        else:
            # DPAPI blob
            try:
                plain = dpapi_unprotect(encrypted_value)
                if isinstance(plain, bytes):
                    return plain.decode('utf-8', errors='ignore')
                return str(plain)
            except Exception as e:
                errors.append(('dpapi_decrypt', str(e), traceback.format_exc()))
                return None
    except Exception as e:
        errors.append(('aes_decrypt', str(e), traceback.format_exc()))
        return None

# Extract and write cookies
def export_cookies(key: Optional[bytes]):
    p = PROFILE_ROOT / 'Default' / 'Cookies'
    rows_out = []
    if not p.exists():
        report_lines.append('- Cookies DB not found')
        return rows_out
    conn=sqlite3.connect(str(p))
    c=conn.cursor()
    try:
        for r in c.execute('SELECT host_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly FROM cookies'):
            host, name, value, encrypted_value, pathf, expires, is_secure, is_httponly = r
            dec = None
            try:
                if encrypted_value:
                    dec = decrypt_value(encrypted_value, key)
                else:
                    dec = value
            except Exception as e:
                errors.append(('cookie_row', str(e), traceback.format_exc()))
            rows_out.append({'host':host,'name':name,'value':dec,'path':pathf,'expires_utc':expires,'is_secure':is_secure,'is_httponly':is_httponly})
    except Exception as e:
        errors.append(('cookies_select', str(e), traceback.format_exc()))
    conn.close()
    # write CSV
    csvf = EXPORT_DIR / 'cookies.csv'
    with open(csvf,'w',encoding='utf-8',newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['host','name','value','path','expires_utc','is_secure','is_httponly'])
        w.writeheader()
        for row in rows_out:
            w.writerow(row)
    report_lines.append(f'- Cookies exported: {len(rows_out)} rows -> {csvf}')
    return rows_out

# Extract and write logins
def export_logins(key: Optional[bytes]):
    p = PROFILE_ROOT / 'Default' / 'Login Data'
    rows_out = []
    if not p.exists():
        report_lines.append('- Login Data DB not found')
        return rows_out
    conn=sqlite3.connect(str(p))
    c=conn.cursor()
    try:
        for r in c.execute('SELECT id, origin_url, action_url, username_value, password_value, signon_realm, date_created FROM logins'):
            id_, origin, action, username, password_value, realm, created = r
            dec = None
            try:
                dec = decrypt_value(password_value, key)
            except Exception as e:
                errors.append(('login_row', str(e), traceback.format_exc()))
            rows_out.append({'id':id_,'origin_url':origin,'action_url':action,'username':username,'password':dec,'signon_realm':realm,'date_created':created})
    except Exception as e:
        errors.append(('logins_select', str(e), traceback.format_exc()))
    conn.close()
    csvf = EXPORT_DIR / 'logins.csv'
    with open(csvf,'w',encoding='utf-8',newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['id','origin_url','action_url','username','password','signon_realm','date_created'])
        w.writeheader()
        for row in rows_out:
            w.writerow(row)
    report_lines.append(f'- Logins exported: {len(rows_out)} rows -> {csvf}')
    return rows_out

# Extract autofill / addresses / credit cards from Web Data
def export_webdata(key: Optional[bytes]):
    p = PROFILE_ROOT / 'Default' / 'Web Data'
    out = {'autofill':[], 'credit_cards':[], 'addresses':[]}
    if not p.exists():
        report_lines.append('- Web Data DB not found')
        return out
    conn=sqlite3.connect(str(p))
    c=conn.cursor()
    try:
        # autofill
        try:
            for r in c.execute('SELECT name, value FROM autofill'):
                out['autofill'].append({'name':r[0],'value':r[1]})
        except Exception:
            pass
        # credit cards
        try:
            for r in c.execute('SELECT guid, name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards'):
                guid,name,exp_m,exp_y,enc = r
                dec = decrypt_value(enc, key) if enc else None
                out['credit_cards'].append({'guid':guid,'name_on_card':name,'exp_month':exp_m,'exp_year':exp_y,'number':dec})
        except Exception:
            pass
        # addresses
        try:
            for r in c.execute('SELECT guid, language_code, label FROM addresses'):
                out['addresses'].append({'guid':r[0],'language_code':r[1],'label':r[2]})
        except Exception:
            pass
    except Exception as e:
        errors.append(('webdata_query', str(e), traceback.format_exc()))
    conn.close()
    # write CSVs
    with open(EXPORT_DIR / 'autofill.csv','w',encoding='utf-8',newline='') as fh:
        w=csv.DictWriter(fh, fieldnames=['name','value'])
        w.writeheader()
        for r in out['autofill']:
            w.writerow(r)
    with open(EXPORT_DIR / 'credit_cards.csv','w',encoding='utf-8',newline='') as fh:
        w=csv.DictWriter(fh, fieldnames=['guid','name_on_card','exp_month','exp_year','number'])
        w.writeheader()
        for r in out['credit_cards']:
            w.writerow(r)
    with open(EXPORT_DIR / 'addresses.csv','w',encoding='utf-8',newline='') as fh:
        w=csv.DictWriter(fh, fieldnames=['guid','language_code','label'])
        w.writeheader()
        for r in out['addresses']:
            w.writerow(r)
    report_lines.append(f"- Web Data exported: autofill {len(out['autofill'])}, credit_cards {len(out['credit_cards'])}, addresses {len(out['addresses'])}")
    return out

# Save raw binary files
def export_raw_files():
    candidates = ['Default/trusted_vault.pb','Default/passkey_enclave_state']
    saved = []
    for c in candidates:
        p = PROFILE_ROOT / c
        if p.exists():
            try:
                dest = RAW_DIR / Path(c).name
                dest.write_bytes(p.read_bytes())
                saved.append(str(dest))
            except Exception as e:
                errors.append(('raw_save', str(e), traceback.format_exc()))
    report_lines.append(f"- Raw files saved: {len(saved)} -> {RAW_DIR}")
    return saved

# main
local_state = PROFILE_ROOT / 'Local State'
report_lines.append('# Extraction Report')
report_lines.append(f'- Profile path: {PROFILE_ROOT}')
report_lines.append('')
key = get_local_state_key(local_state)
if key:
    report_lines.append('- Local State AES key extracted successfully.')
else:
    report_lines.append('- Failed to extract Local State key. Some decryption may fail.')

cookies = export_cookies(key)
logins = export_logins(key)
webdata = export_webdata(key)
raws = export_raw_files()

# summarize
report_lines.append('\n## Summary')
report_lines.append(f'- Cookies: {len(cookies)}')
report_lines.append(f'- Logins: {len(logins)}')
report_lines.append(f'- Autofill rows: {len(webdata.get("autofill",[]))}')
report_lines.append(f'- Credit cards found: {len(webdata.get("credit_cards",[]))}')
report_lines.append(f'- Addresses found: {len(webdata.get("addresses",[]))}')
report_lines.append(f'- Raw files saved: {len(raws)}')

if errors:
    report_lines.append('\n## Errors & Notes')
    for e in errors:
        report_lines.append(f'- {e[0]}: {e[1]}')

# write report
with open(EXPORT_DIR / 'report.md','w',encoding='utf-8') as fh:
    fh.write('\n'.join(report_lines))

print('Export complete. Files in', EXPORT_DIR)
print('Report summary:')
for l in report_lines[:20]:
    print(l)
