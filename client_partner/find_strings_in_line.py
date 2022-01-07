

def find_strings_in_line(line, previous_line, partners_dict):
    for key in partners_dict:
        if len( partners_dict[key]['strings'] ) == 0:
            pass
        else:
            for string_list in partners_dict[key]['strings']:
                found_all = True

                if len( string_list ) == 0:
                    found_all = False

                for string in string_list:
                    if string not in line:
                        found_all = False
                        # brake # stop looping strings for this vendot
                if found_all == True:
                    return key

    return False