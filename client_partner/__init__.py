
"""
                Import all functions, classes, etc from all files in the current directory
"""


# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
"""Import all modules that exist in the current directory."""
# Ref https://stackoverflow.com/a/60861023/
from importlib import import_module
from pathlib import Path

parent_folder_name = Path(__file__).parent.name

for f in Path(__file__).parent.glob("*.py"):
    module_name = f.stem

    # print()
    # print('module name before importing ==> ', module_name)
    # # print(' globals ==> ', globals() )
    # print()


    """ The problem with not importing a module with a name that already is in globals() :
        Sometimes we have used a function in another file with a relative import.
        Then it is already in globals()
        If we dont import it here then python gives an error that the module is not callable.
        Need to research more on that.

    # if (not module_name.startswith("_")) and (module_name not in globals()):
    """

    if not module_name.startswith("_"):
        mdl = import_module(f".{module_name}", __package__)
    
        # print()
        # print('Imported Module ==> ' + module_name + ' in __init__.py file of ' + parent_folder_name)
        # print()

        # https://stackoverflow.com/questions/43059267/how-to-do-from-module-import-using-importlib
        # get a handle on the module
        # mdl = importlib.import_module('X')
        # is there an __all__?  if so respect it
        if "__all__" in mdl.__dict__:
            names = mdl.__dict__["__all__"]
        else:
            # otherwise we import all names that don't begin with _
            names = [x for x in mdl.__dict__ if not x.startswith("_")]
        # now drag them in
        globals().update({k: getattr(mdl, k) for k in names})


    del f, module_name
del import_module, Path
