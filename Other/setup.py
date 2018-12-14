import cx_Freeze, os
os.environ['TCL_LIBRARY'] = r'C:\Users\User\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\User\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
executables = [cx_Freeze.Executable("Orbit_Simv5.py")]

additional_mods = ['numpy.core._methods', 'numpy.lib.format']
cx_Freeze.setup(
    name="Asteroids",
    options={"build_exe": {"packages": ["pygame"], "include_files": ['background1.png'], 'includes': additional_mods}},
    executables=executables,
    version="1.0.0"
)