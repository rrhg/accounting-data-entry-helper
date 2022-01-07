import json


def write_list_to_json_file( alist, file):
    # make_bakup(file)
    try:
        with open(file, '+w', newline='\n', encoding='utf-8') as f:
            json.dump( alist, f, indent=4)
    except Exception as e:
        print()
        print(" Could not write list to json file in utils.write_list_to_json_file. error == ", e )
        print()
        # exit()
