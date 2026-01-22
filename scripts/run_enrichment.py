#!/usr/bin/env python3
"""
Run enrichment: Top Sites sync, Autofill entropy, Shortcuts generation, Local Storage injection.
"""
from pathlib import Path
import sys
import os
# Ensure repo root in sys.path for module imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

profile = Path('generated_profiles/37ab1612-c285-4314-b32a-6a06d35d6d84')
if not profile.exists():
    print('Profile not found:', profile)
    sys.exit(1)

history_db = profile / 'Default' / 'History'
top_sites_db = profile / 'Default' / 'Top Sites'
web_data_db = profile / 'Default' / 'Web Data'
shortcuts_path = profile / 'Default' / 'Shortcuts'
leveldb_dir = profile / 'Default' / 'Local Storage' / 'leveldb'

print('[ENRICH] Syncing Top Sites...')
from tools.top_sites_sync import sync_top_sites
sync_top_sites(str(history_db), str(top_sites_db))
print('  > Top Sites synced')

print('[ENRICH] Injecting autofill entropy...')
from tools.autofill_entropy import inject_autofill
inject_autofill(str(web_data_db))
print('  > Autofill injected')

print('[ENRICH] Generating Shortcuts binary...')
from tools.shortcuts_gen import generate_shortcuts
generate_shortcuts(str(shortcuts_path))
print('  > Shortcuts generated')

print('[ENRICH] Generating Local Storage keys...')
from tools.state_architect import generate_all
from tools.leveldb_writer import write_local_storage
keys = generate_all()
ok = write_local_storage(str(leveldb_dir), keys)
print('  > Local Storage written:', ok)

print('[ENRICH] Done')
