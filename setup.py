import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py", base=base)]

cx_Freeze.setup(
    name="Eagle Eye",
    options={"build_exe": {"packages":["tkinter", "cv2", "PIL", "numpy", "re", "os"],
                           "include_files":["user_gui.py", "gui_builder.py", "timestamp_ops.py",
                                            "config.py"]}},
    version="0.04",
    description="Store map image traversal application",
    executables=executables
)
