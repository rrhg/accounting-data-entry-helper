

def find_customer_in_line( customers_dict, line):
    found = True

    for key in customers_dict:
        customer = customers_dict[key]
        # print(str(  customer   ))
        if len( customer['strings'] ) == 0:
            found = False
        else:
            for string_list in customer['strings']:
                for s in string_list:
                    if s not in line:
                        found = False
                if found:
                    # print('key found == ' + key)
                    return key

    return False