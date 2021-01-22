import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options=dict(packages=["os"], excludes=["tkinter"])

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    name="sonos-pair",
    version="1.0",
    description="A Sonos pairing application",
    options=dict(build_exe=build_exe_options),
    executables=[Executable("sonos_pair.py", base=base, target_name="sonos-pair")],
)
