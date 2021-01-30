import os
import sys
from cx_Freeze import setup, Executable

build_exe_options = dict(
    include_files=["assets"],
    excludes=["tcl", "ttk", "tkinter", "Tkinter"],
)
bdist_mac_options = dict(
    iconfile="space_invaders.icns",
    bundle_name="Space Invaders",
)

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"


executables = [
    Executable(
        script="main.py",
        base=base,
        icon="space_invaders.icns",
        shortcut_name="Space Invaders",
        target_name="Space Invaders",
    )
]

setup(
    name="Space Invaders",
    options={"bdist_mac": bdist_mac_options, "build_exe": build_exe_options},
    executables=executables,
)
