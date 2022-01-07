

def line_contains_all_strings(list_of_strings, line):
    found_all = True
    for s in list_of_strings:
        if s not in line:
            found_all = False
    # if found_all == True:
    #     pass
    return found_all