import re
from config import client
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

    def log_and_train(self, line):
        self.print_trans_added(line)
        self.train_model(line)

    def train_model(self, line):
        data_list = [ line, self.partner_code ]
        # TODO: train model.
        # Do not save model here
        # Save only once, when script finish- should we ask to save?        


    def print_trans_added(self, line):
        print()
        print('transaction added --->> ')
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                if not attr == 'internal_period_number':
                    print(attr, '=', value)
        print()
        print('line was --->> ')
        print( line )
        print('==========================')
        print()
