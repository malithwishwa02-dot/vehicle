"""Make a cleaned copy of the profile folder excluding caches and large binaries.

Usage: python make_clean_copy.py

Creates directory: <source>-clean
Writes log of removed files to removed_files.txt in destination.
"""
import os, shutil
from pathlib import Path

SRC = Path(r"d:\vehicle\37ab1612-c285-4314-b32a-6a06d35d6d84")
DST = SRC.parent / (SRC.name + '-clean')
EXCLUDE_DIRS = {
    'Cache', 'Cache\Cache_Data', 'Code Cache', 'GPUCache', 'GrShaderCache', 'ShaderCache',
    'DawnGraphiteCache', 'DawnWebGPUCache', 'BrowserMetrics', 'BrowserMetrics-spare.pma',
    'Crashpad\\attachments', 'Crashpad\\reports', 'component_crx_cache', 'Cache\\Cache_Data'
}
# Maximum file size to include (bytes) unless special case
MAX_SIZE = 2 * 1024 * 1024  # 2 MB
KEEP_IF_LARGE = {'.db', 'Local State', 'Preferences', 'Last Version', 'Last Browser', 'trusted_vault.pb', 'passkey_enclave_state'}

removed = []
copied = []

if DST.exists():
    print('Removing existing destination', DST)
    shutil.rmtree(DST)

for root, dirs, files in os.walk(SRC):
    rel = os.path.relpath(root, SRC)
    # Skip excluded directories by checking top-level segment names
    parts = rel.split(os.sep)
    if parts[0] == '.':
        parts = []
    skip = False
    for ex in EXCLUDE_DIRS:
        # allow matching if ex is substring of rel or directory name
        if ex and ex in rel:
            skip = True
            break
    if skip:
        # record that this directory is removed
        removed.append((root, 'dir_excluded'))
        continue
    # create destination dir
    dest_dir = DST.joinpath(rel)
    dest_dir.mkdir(parents=True, exist_ok=True)
    for f in files:
        srcf = Path(root) / f
        dstf = dest_dir / f
        try:
            sz = srcf.stat().st_size
        except Exception:
            sz = 0
        keep = False
        if f in KEEP_IF_LARGE or any(f.endswith(s) for s in KEEP_IF_LARGE if s.startswith('.')):
            keep = True
        if sz > MAX_SIZE and not keep:
            removed.append((str(srcf), f'size_{sz}'))
            continue
        # copy file
        try:
            shutil.copy2(srcf, dstf)
            copied.append((str(dstf), sz))
        except Exception as e:
            removed.append((str(srcf), f'copy_err:{e}'))

# write removed files log
DST.mkdir(parents=True, exist_ok=True)
with open(DST / 'removed_files.txt','w',encoding='utf-8') as fh:
    fh.write('Removed or excluded items during clean copy:\n')
    for r in removed:
        fh.write(str(r) + '\n')

# write README for cleaned folder
with open(DST / 'README_CLEANED.txt','w',encoding='utf-8') as fh:
    fh.write('This cleaned profile copy excludes large cache folders and binary caches to reduce size.\n')
    fh.write('Excluded directory patterns: ' + ', '.join(EXCLUDE_DIRS) + '\n')
    fh.write('Files larger than 2MB were excluded unless in KEEP_IF_LARGE set.\n')

# summary
total_removed = len(removed)
total_copied = len(copied)
print('Clean copy created at', DST)
print('Files copied:', total_copied)
print('Files/dirs removed/skipped:', total_removed)
print('See', DST / 'removed_files.txt')
