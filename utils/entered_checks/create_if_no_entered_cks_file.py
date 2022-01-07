from os import path
from utils.json import get_dict_from_json_file
from utils.json import write_dict_to_json_file


def create_if_no_entered_cks_file( file ):

    if not path.exists( file ):
        adict = {}
        write_dict_to_json_file(adict, file)
    else:
        pass