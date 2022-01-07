from .get_csv_rows import get_csv_rows


# TODO delete file ??

def get_and_clear_csv_rows(file):
    rows = get_csv_rows( file )
    for r in rows:


        """ TODO maybe it should be 
        fields_to_clear = client.get_csv_fields_to_clear() or something ike that
        """
        
        r[23] = '1' # field 23 in all rows is the number of sub-transactioms(invoices, aka account line) in the transaction. Many consecuence transactions had the same number(15) & peachtree put them all together
        # clear fields that should not have values
        fields_to_clear = {'code': 0, 'name1': 1, 'name2':2, 'addr1':3, 'addr2':4, 'ck number':9, 'date1':10, 'memo':15, 'date2':21, 'line-invoice-description':28, 'account':29, 'amount':33, 'period':36, 'transaction_number':37 }  
        for i in fields_to_clear.values(): #[0,         1,         2,           9,          10,         15,      21,                              28,            29,          33,          36,                      37]:
            r[i] = "" 
    return rows

