


def add_module_attrs_to_globals(module, globals_dict): 
    # https://stackoverflow.com/questions/43059267/how-to-do-from-module-import-using-importlib
    # is there an __all__?  if so respect it
    if "__all__" in module.__dict__:
        names = module.__dict__["__all__"]
    else:
        # otherwise we import all names that don't begin with _
        names = [x for x in module.__dict__ if not x.startswith("_")]

    # now drag them in
    globals_dict.update({k: getattr(module, k) for k in names})



# NOTE: below is another version with code that could work for any dir
#    (not just current), but still has a bug
def import_files_in_curr_dir(path_obj, __package__):
    """
        Import all functions(objs), classes, etc 
        from all files in the current directory
            https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
            Import all modules that exist in the current directory
            Ref https://stackoverflow.com/a/60861023/
    """

    # TODO: why can't import this at top of file
    from importlib import import_module
    from pathlib import Path

    modules = {}
    parent_folder_name = path_obj.name

    for f in path_obj.glob("*.py"):
        module_name = f.stem

        if not module_name.startswith("_"):
            module = import_module(f".{module_name}", __package__)

            modules[ module_name ] = module

        del f, module_name

    del import_module, Path
    return modules
    # return module



def import_files_in_dir(path_obj, __package__):

    """
        NOTE: another version with code that could work for any dir
        (not just current), but still has a bug.
        
    """

    from importlib import import_module
    from pathlib import Path

    """
        Import all functions(objs), classes, etc 
        from all files in a directory
    """

    """
        The problem here is when imported modules
        relative imports.
        ImportError: attempted relative import with no known parent package
        TODO: fix if want to shorter client.py code
    """

    # https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
    # Import all modules that exist in the current directory
    # Ref https://stackoverflow.com/a/60861023/

    all_objs_names = []

    parent_folder_name = path_obj.name


    for f in path_obj.glob("*.py"):
        module_name = f.stem

        """ 
        Todo: The problem with not importing a module with a name that already is in globals() : Sometimes we have used a function in another file with a relative import. Then it is already in globals().  If we dont import it here then python gives an error that the module is not callable.  Need to research more on that.
        # if (not module_name.startswith("_")) and (module_name not in globals()):
        """

        if not module_name.startswith("_"):
            # print('======================')
            # print('__package__ ==> ')
            # print(__package__)
            # print('======================')

            # old way of importing
            # mdl = import_module(f".{module_name}", str(path_obj))
            # mdl = import_module(f".{module_name}", __package__)

            file_name = str(module_name) + '.py'
            module_path = path_obj / file_name

            # print('==================')
            # print('module name to be imported')
            # print(module_name)
            # print('==================')
            # print(f'importing all from {str(path_obj)}')
            # print('==================')
        

            # this code was giving this error:
            # ImportError: attempted relative import with no known parent package     
            # posible fix # https://stackoverflow.com/questions/50884100/using-importlib-to-dynamically-import-modules-containing-relative-imports       
            import importlib.util
            # spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
            spec = importlib.util.spec_from_file_location(module_name, str(module_path)  )
            mdl = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mdl)
            # foo.MyClass()


            # print()
            # print('Imported Module ==> ' + module_name + ' in __init__.py file of ' + parent_folder_name)
            # print()

            all_objs_names.extend( [n for n in names] )

        del f, module_name
    del import_module, Path
    return all_objs_names
