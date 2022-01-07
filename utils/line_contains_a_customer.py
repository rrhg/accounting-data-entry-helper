

def line_contains_a_customer( customers_dict, line):
    # print(str( customers_dict   ))
    found = True

    for key in customers_dict:
        customer = customers_dict[key]
        # print(str(  customer   ))
        if len( customer['strings'] ) == 0:
            found = False
        else:
            for string_list in customer['strings']: # customer can have 1 or more list of strings
                found = True
                for s in string_list: # if ALL these strings are in line, then we found a customer
                    if s not in line:
                        found = False

                if found:
                    # print('key found == ' + key)
                    return key

    return False