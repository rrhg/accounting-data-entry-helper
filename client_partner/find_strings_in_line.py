

def find_strings_in_line(line,
                         previous_line,
                         partners_dict,
                         is_check=False,
                         infered_payee_in_ck_image=""):

    if is_check:
        print(f"\n infered_payee_in_ck_image: =>{infered_payee_in_ck_image}<=. Make sure is empty str if not found. Bc if this returns other than '' when finds nothing, here, we could wrongly find a match for a wrong vendor")
        if infered_payee_in_ck_image == "":
            return False
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