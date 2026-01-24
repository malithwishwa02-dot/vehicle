# -- mode: python ; coding: utf-8 --
block_cipher = None

a = Analysis(
    ['windows/lucid_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('interface/', 'interface/'),  # Include Dashboard HTML
        ('core/', 'core/'),            # Include Logic
        ('bin/', 'bin/'),              # Include RunAsDate & Firefox
        ('modules/', 'modules/'),
        ('tools/', 'tools/')
    ],
    hiddenimports=['engineio.async_drivers.threading', 'flask', 'webview', 'playwright'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LucidEmpire',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Hides the Black Console Window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' # Ensure you have an icon
)
