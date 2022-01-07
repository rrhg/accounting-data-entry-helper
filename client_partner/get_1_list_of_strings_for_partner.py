

def get_1_list_of_strings_for_partner(ptype):
    user_strings = []
    while True:
        print()
        a = str( input("(y or [enter] for no) Do u want to enter another unique string(combination of characters) to find this "+ ptype +" in a line ?: (Note: the code & name have allready been added....  What u can add here is additional strings that will be included together as a another list to check) : " ) )
        
        if a == 'y' or a == 'Y':
            string1 = str( input(" Enter a string : " ) )
            user_strings.append(string1)
        else:
            break
            
    return user_strings