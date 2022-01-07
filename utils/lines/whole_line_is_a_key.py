
def whole_line_is_a_key(line, vendors_dict):
    #if line in vendors_dict: return True
    found_keys = [key for key in vendors_dict.keys() if line == key or key in line]
    if found_keys: return found_keys[0]
    return False
