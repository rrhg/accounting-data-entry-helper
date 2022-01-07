# import json
from .write_dict_to_json_file import write_dict_to_json_file

# TODO : rename. clear_dict_in_json_file ??
def clear_json_file(file):

    empty_dict = {}

    write_dict_to_json_file( empty_dict, file)