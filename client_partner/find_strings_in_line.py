

def find_strings_in_line(line,
                         previous_line,
                         partners_dict,
                         infered_payee_in_ck_image=""):

    if (infered_payee_in_ck_image == "could not infer payee from check"
        or
        infered_payee_in_ck_image != ""
        ):
        # is a check
        line_to_search = infered_payee_in_ck_image
        
    else: # is a non check line
        line_to_search = line
    
    for key in partners_dict:
        if len( partners_dict[key]['strings'] ) == 0:
            pass
        else:
            for string_list in partners_dict[key]['strings']:
                found_all = True

                if len( string_list ) == 0:
                    found_all = False

                for string in string_list:
                    if string not in line_to_search:
                        found_all = False
                        # brake # stop looping strings for this vendor
                if found_all == True:
                    return key

    return False