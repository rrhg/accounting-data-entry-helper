

def csv_to_space_separated_txt_file(in_file, out_file):
    rows_of_lists = get_csv_rows(in_file, del_headers=True)
    rows_of_txt = []
    
    for l in rows_of_lists:
        txt = ' '.join(l)
        txt = txt + '\n'
        rows_of_txt.append(txt)

    with open(out_file, '+w', newline='\n', encoding='utf-8') as f:
        for t in rows_of_txt:
            f.write(t)

csv_ext = '.csv'
txt_ext = '.txt'

#TODO create client.csv_statement_file()
csv_file = r"C:\Users\path\to\file"


in_file = csv_file + csv_ext
out_file = csv_file + txt_ext


if __name__ == '__main__':
    from get_csv_rows import get_csv_rows # for when calling this file directly from terminal & in this dir
    csv_to_space_separated_txt_file(in_file, out_file)
