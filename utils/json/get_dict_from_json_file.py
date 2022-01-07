import json
from os.path import exists
from .write_dict_to_json_file import write_dict_to_json_file


def get_dict_from_json_file(file):
    # print('file == '+ file)
    d = {}
    if not exists(file):
        """ create file & write an empty dict """
        write_dict_to_json_file( d, file) 

    with open(file, 'r') as f:
        d = dict( json.load( f ) )
    # print('d == ', d)
    return d