from config import client, customer
from client_partner.add_partner import add_to_json_file
from utils.csv2.get_csv_rows import get_csv_rows
from client_partner.partner_dict import partner_dict



def main():
    csv_file = client.file_with_new_customers_to_import()
    rows = get_csv_rows( csv_file )
    """ csv rows have been converted to lists """
    
    customers = []
    for r in rows:
        new_partner_dict = client.convert_imported_customer_csv_row_to_dict( r, partner_dict )
        customers.append( new_partner_dict )

    for c in customers:
        # print( c['code'], c['name'], c['account'] )
        add_to_json_file( c, ptype=customer) # to update file with all partners(do we need a database?) 
        """ Append, do not overwrite. There is one harcoded -> create new """

if __name__ == '__main__':
    main()
