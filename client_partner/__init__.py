from pathlib import Path
from utils.files.import_files_in_curr_dir import (
    import_files_in_curr_dir,
    add_module_attrs_to_globals
)

"""
    Import all file modules in current dir
    & and make their attributes available in globals.
    * Same as < from ./afile.py import * > but for all files 
    * Otherwise a bad practice but in this case allows
    for faster development & attributes are unlikely to 
    have same names. 
"""

globals_dict = globals()
parent = Path(__file__).parent
imported_modules = import_files_in_curr_dir(parent, __package__)
for name, module in imported_modules.items():
    add_module_attrs_to_globals(module, globals_dict)