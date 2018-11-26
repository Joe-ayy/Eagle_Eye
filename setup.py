import cx_Freeze
import sys
import os

os.environ['TCL_LIBRARY'] = r'C:\Program Files (x86)\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files (x86)\Python36\tcl\tk8.6'

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py", base=base)]

cx_Freeze.setup(
    name="Eagle Eye",
    options={"build_exe": {"packages":["tkinter", "cv2", "PIL", "numpy", "re", "os"],
                           "include_files":["file_handler.py", "user_gui.py", "gui_builder.py", "timestamp_ops.py",
                                            "config.py", "tcl86t.dll", "tk86t.dll"]}},
    version="0.04",
    description="Store map image traversal application",
    executables=executables
)
