# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller 配置文件 - VRC心率OSC工具
用于将 Python 应用打包为独立的 Windows 可执行文件
"""

block_cipher = None

a = Analysis(
    ['VRC_HR_Tool_SinkStar101_pyqt_single.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.ini', '.'),  # 包含配置文件模板
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'bleak',
        'bleak.backends',
        'bleak.backends.winrt',
        'pythonosc',
        'pythonosc.udp_client',
        'websocket',
        'websocket._app',
        'pulsoid_worker',
        'asyncio',
        'configparser',
    ],
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
    name='VRC_HR_Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 显示控制台窗口以便查看日志
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如果有图标文件，可以在这里指定路径
)
