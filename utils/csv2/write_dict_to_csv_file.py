import re
import csv


def write_dict_to_csv_file(dict_data, file):
    try:
        # with open(file, 'w') as f:
        with open(file, '+w', newline='\n', encoding='utf-8') as f:
            # writer = csv.DictWriter(f)
            # w = csv.writer(f, lineterminator='\n')            
            writer = csv.DictWriter(f, lineterminator='\n', fieldnames=['code', 'name', 'account', 'description'])
            # writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print(" Could not write dict to csv file")