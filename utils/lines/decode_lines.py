from .is_not_a_blanc_line import is_not_a_blanc_line

def decode_lines(statement_text_file):
    lines = []
    with open(statement_text_file, 'rb') as f:
        # print(f.readlines()) # it was giving this error: UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 6450: character maps to <undefined>
        for ln in f:
            decoded=False
            line='line not decoded'
            for cp in ('cp1252', 'cp850','utf-8','utf8'):
                try:
                    line = ln.decode(cp)
                    decoded=True
                    break
                except UnicodeDecodeError:
                    pass
            
            if decoded and is_not_a_blanc_line(line):
                lines.append(line)
    return lines