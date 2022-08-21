from config import vendor, customer, debit, credit, client, model
import utils
from .prompt_user_for_partner_autocomplete import prompt_user_for_partner_autocomplete
from .create_and_add_partner import create_and_add_partner
from utils.lines.ignored_lines import ignored_lines
from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")


"""    Reminder:
        clients == our accounting clients
        partner(type == customers) == customers to our clients
        partner(type == vendors) == vendors to our clients
"""


def ask_to_create_partner_or_ignore_line(line, previous_line, ptype=vendor, msg_if_not_found=''):

    predicted_vendor_code = model.predict_partner(line) # we r still not using previous line to train the model. only the line for now.

    print()    
    if msg_if_not_found:
        red.print(msg_if_not_found)
    else:
        red.print('Found NO '+ ptype +' for this line:')

    print(line)
    print()
    red.print('1- Choose a '+ ptype )
    red.print('2- Choose the suggested '+ptype+' :'+ str(predicted_vendor_code) )
    red.print('3- Ignore line for ever (add line to ignored lines)')
    red.print('4- Ignore line just this time')
    # red.print('6- Test the model')


    while True:
        print()
        red.print('Enter a number from 1 to 4: ')
        a = str( input(' : ') )
    
        if a == '1': 
            partner_key = prompt_user_for_partner_autocomplete( 'this line', ptype=ptype)

            if partner_key == 'create new vendor' or partner_key == 'create new customer':
                partner_info_dict = create_and_add_partner( line, previous_line, ptype=ptype ) # get info from user. Pass an '' bc is expecting the line(as a string) but in a check we dont have vendor info
                # TODO fix partner_info_dict ===>>>>> {'code': code, 'name': name, 'memo':memo, 'account': account, 'type': vtype, 'strings': strings }
                partner_key = partner_info_dict['code']
            return partner_key
            

        if a == "2":
            partner_key = predicted_vendor_code 
            return partner_key


        if a == '3':
            print()
            red.print('ignoring line forever by adding it to ignored lines json file')
            print( repr(line) )

            ttype = debit
            if ptype == customer:
                ttype = credit
            i = ignored_lines(ttype=ttype)
            i.add(line)
            print()
            return False


        if a == '4':                    
            print()
            red.print('Ignoring line just this time')
            print()
            return False


        # if a == '6':
        #     print()
        #     l = input(' Enter a line to make a prediction')
        #     test_prediction = model.predict_partner(l)
        #     yellow.print('predicted == ', test_prediction)
        #     model.print_partners_prob(line)
        #     print()
        #     """ Do nothing. While loop will ask again"""
        #     # return False 