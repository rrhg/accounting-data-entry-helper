from config import client


def order_checks_lines( lines ):
    list1 = []
    list2 = []
    merged = []
    for line in lines:
        ck1 = client.get_1st_ck_line_from_line(line)
        list1.append(ck1)

        if client.line_has_more_than_1_ck( line ): 
            ck2 = client.get_2nd_ck_line_from_line(line)
            list2.append(ck2)

    merged.extend(list1)
    merged.extend(list2)
    return merged