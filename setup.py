import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"include_files": ["settings.json"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32" or sys.platform == "win64":
    base = "Win32GUI"

setup(name="Power Core Omega",
      version="0.0.1",
      optimize=2,
      description="Power Core Omega Ultra Early Alpha",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])
