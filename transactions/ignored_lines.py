from config import debit, credit, IGNORED_DEBIT_LINES_FILE, IGNORED_CREDIT_LINES_FILE
from utils.json.write_list_to_json_file import write_list_to_json_file
from utils.json.get_list_from_json_file import get_list_from_json_file


def get_ignored_lines( trans_type=debit ):
    f = IGNORED_DEBIT_LINES_FILE
    if trans_type == credit:
        f = IGNORED_CREDIT_LINES_FILE
    l = get_list_from_json_file( f )
    return l


def add_ignored_debit_line( astring, trans_type=debit ):
    lines = get_ignored_lines( trans_type=trans_type ) # from the json file
    lines.append( astring )
    lines = sorted( lines )
    f = IGNORED_DEBIT_LINES_FILE
    if trans_type == credit:
        f = IGNORED_CREDIT_LINES_FILE
    write_list_to_json_file( lines, f )


def line_is_in_ignored_lines(line, trans_type=debit):

    # lines_to_ignore . these lines are between debits first line & last line only, & we already looked for vendors in them, & may not have a vendor
    lines_to_ignore = get_ignored_lines( trans_type=trans_type )

    for ignored_line in lines_to_ignore:
        if line == ignored_line:
            return True
    
    return False


def remove_ignored_lines(lines, trans_type=debit):
    l = []
    for line in lines:
        if line_is_in_ignored_lines(line, trans_type=trans_type):
            pass
        else:
            l.append(line)
    return l