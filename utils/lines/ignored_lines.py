from config import IGNORED_CREDIT_LINES_FILE, IGNORED_DEBIT_LINES_FILE, debit, credit, vendor, customer
from utils.json.write_list_to_json_file import write_list_to_json_file
from utils.json.get_list_from_json_file import get_list_from_json_file


class ignored_lines():
    """ Lines to ignore . User can add a line to a json file containing lines to ignore. These lines will be removed from the lines used for search transactions. Usually are lines are between first line & last line only, & we already looked for vendors or customer in them, & may not have or doesn't make sense to search """
    def __init__(self, ttype=debit ):
        self.file = IGNORED_DEBIT_LINES_FILE
        if ttype == credit:
            self.file = IGNORED_CREDIT_LINES_FILE
        self.ttype = ttype

    def get_all(self):
        l = get_list_from_json_file( self.file )
        return l

    def add(self, astring ): # a line is a string
        lines = self.get_all() # from the json file
        lines.append( astring )
        lines = sorted( lines )
        write_list_to_json_file(  lines, self.file  )

    def contains(self, line): # line is a string
        lines_to_ignore = self.get_all()

        for ignored_line in lines_to_ignore:
            if line == ignored_line:
                return True
        
        return False