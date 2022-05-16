from pathlib import Path
from utils.files.import_files_in_curr_dir import import_files_in_curr_dir

parent = Path(__file__).parent
functions_modules = import_files_in_curr_dir(parent, __package__)
