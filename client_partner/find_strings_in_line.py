

def find_strings_in_line(line,
                         previous_line,
                         partners_dict,
                         infered_payee_in_ck_image=""):

    partner_line = line if not infered_payee_in_ck_image else infered_payee_in_ck_image
    
    for key in partners_dict:
        if len( partners_dict[key]['strings'] ) == 0:
            pass
        else:
            for string_list in partners_dict[key]['strings']:
                found_all = True

                if len( string_list ) == 0:
                    found_all = False

                for string in string_list:
                    if string not in partner_line:
                        found_all = False
                        # brake # stop looping strings for this vendor
                if found_all == True:
                    return key

    return False