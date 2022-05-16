from pathlib import Path
from .functions import functions_modules


class client:
    name = Path(__file__).parent.name # parent_folder_name

"""
    Assign all functions & objects
    defined in all files in <client name>/functions
    as attributes of client
    because are used as settings that varies depending on accounting client
"""
for mod_name, module in functions_modules.items():
    functions = [{'name':name, 'obj':attr} for name,attr in module.__dict__.items() if not name.startswith('_')] 
    for f in functions:
        setattr(client, f['name'], f['obj'])