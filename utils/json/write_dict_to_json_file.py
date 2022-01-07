import json


def write_dict_to_json_file(a_dict, file):

        with open(file, '+w', newline='\n', encoding='utf-8') as f:

            json.dump( a_dict, f, indent=4)

