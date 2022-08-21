from .create_or_clear_file import create_or_clear_file
from .get_clients_names_from_dir import get_clients_names_from_dir
from .get_sub_directories import get_sub_directories
from .create_dir_w_parents import create_dir_w_parents
from pathlib import Path


def get_last_file_obj_in_dir(dir_path_:str):
    dir_obj = Path(dir_path_)
    last_file = ''
    for child in dir_obj.iterdir():
        if child.is_file():
            last_file = child
    if not last_file: raise Exception(f'Did not found a file in {str(dir_obj)}')
    return last_file

