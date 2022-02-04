import re
from config import client, model
from utils.csv2.write_rows_to_csv_file import write_rows_to_csv_file
from utils.csv2.append_csv_row_to_file import append_csv_row_to_file

# TODO should this have defaults for credits & debits ? 
class transaction:
    line_has_2_debits = False # TODO can this be deleted
    partner_key = ''
    partner_code = ''
    partner_name = ''
    amount = ''
    ck_number = ''
    is_check = False 
    date = ''
    memo = '' 
    account = ''
    found = True # TODO can this be deleted
    bank_account = ''
    internal_period_number = ''
    transaction_number = ''

    def log_and_train(self, line, previous_line):
        self.print_trans_added(line, previous_line)
        self.train_model(line, previous_line)

    def train_model(self, line, previous_line):
        # TODO should we use the previous line to train the model?
        # line = line + previous_line
        # The problem is that in some cases it matters & in others it actually makes it worse

        model.train_model(line, self.partner_code)
        """ 
        Do not save model here
        Save only once, when script finish        
        """

    def print_trans_added(self, line, previous_line):
        print()
        print('==========================')
        print('transaction added --->> ')
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                if not attr == 'internal_period_number':
                    print(attr, '=', value)
        print()
        print('previous line was : ')
        print( previous_line )
        print('line was : ')
        print( line )
        print('==========================')
        print()
