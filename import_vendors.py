from config import client, vendor
from client_partner.add_partner import add_to_json_file
from utils.csv2.get_csv_rows import get_csv_rows
from client_partner.partner_dict import partner_dict


def main():
    csv_file = client.file_with_new_vendors_to_import()
    rows = get_csv_rows( csv_file )
    """ csv rows have been converted to lists """

    vendors = []
    for r in rows:
        new_partner_dict = client.convert_imported_vendor_csv_row_to_dict( r, partner_dict )
        vendors.append( new_partner_dict )


    for c in vendors:
        # print( c['code'], c['name'], c['account'] )
        add_to_json_file( c, ptype=vendor) # to update file with all partners(do we need a database?) 


if __name__ == '__main__':
    main()
