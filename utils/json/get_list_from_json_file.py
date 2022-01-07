import json
from os.path import exists
from .write_list_to_json_file import write_list_to_json_file


def get_list_from_json_file(file):
    # print('file == '+ file)
    l = []
    if not exists(file):
        """ create file & write an empty list """
        write_list_to_json_file( l, file) 

    with open(file, 'r') as f:
        l = list( json.load( f ) )

    return l