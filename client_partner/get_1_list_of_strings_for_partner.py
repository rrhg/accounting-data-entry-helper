from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")


def get_1_list_of_strings_for_partner(ptype):
    user_strings = []
    while True:
        print()
        red.print("( 'y' or 'enter' ) Do u want to enter another unique string(combination of characters) to find this "+ ptype +" in a line ?: (Note: the code & name have allready been added....  What u can add here is additional strings that will be included together as a another list to check) : " )
        a = str( input(" : " ) )
        
        if a == 'y' or a == 'Y':
            print()
            red.print(" Enter a string : " )
            string1 = str( input(" : " ) )
            user_strings.append(string1)
        else:
            break
            
    return user_strings