import json
from .make_bakup import make_bakup


def write_dict_to_json_file(dict_of_dicts, file):
    make_bakup(file)
    
    try:
        with open(file, '+w', newline='\n', encoding='utf-8') as f:
            json.dump(dict_of_dicts, f, indent=4)
    except IOError:
        print(" Could not write dict of dicts to txt file")
        print(" error in write_dict_to_json_file()")

