from .json.get_dict_from_json_file import get_dict_from_json_file


def get_customers_dict(file):
    d = get_dict_from_json_file(file)
    return d