from config import vendor, customer, debit, credit
import utils
from .prompt_user_for_partner_autocomplete import prompt_user_for_partner_autocomplete
from .create_and_add_partner import create_and_add_partner
from utils.lines.ignored_lines import ignored_lines


def ask_to_create_partner_or_ignore_line(line, previous_line, ptype=vendor, msg_if_not_found=''):
    # TODO: predicted_vendor_code = model.predict_partner( line, ptype )
    print()
    if msg_if_not_found:
        print(msg_if_not_found)
    else:
        print('Found NO '+ ptype +' for this line:')

    print(line)
    print()
    # TODO: print('Predicted vendor code == ', predicted_vendor_code)
    print('1- Choose an existing '+ ptype )
    print('2- Create a new '+ ptype)
    print('3- Ignore line for ever (add line to ignored lines)')
    print('4- Ignore line just this time')

    while True:
        a = str( input('Enter 1 or 2 or 3 or 4 : ') )
    
        if a == '1': # = = = = = = = = = = =  = = = =  = = =
            partner_key = prompt_user_for_partner_autocomplete( 'this line', ptype=ptype)


            if partner_key == 'create new vendor':
                partner_info_dict = create_and_add_partner( line, previous_line, ptype=ptype ) # get info from user. Pass an '' bc is expecting the line(as a string) but in a check we dont have vendor info
                # TODO fix partner_info_dict ===>>>>> {'code': code, 'name': name, 'memo':memo, 'account': account, 'type': vtype, 'strings': strings }
                partner_key = partner_info_dict['code'] 
          
            return partner_key
            

        if a == "2":
            print()
            print('==== creating a '+ ptype +' ========================')
            print()
            vendor_dict = create_and_add_partner(line, previous_line, ptype=ptype)

            # vendor_dict ===>>>>> {'code': code, 'name': name, 'memo':memo, 'account': account, 'type': vtype, 'strings': strings }
            partner_key = vendor_dict['code'] # = = = = = = = = = = = = = = = = 

            return partner_key


        if a == '3':
            print()
            print('ignoring line forever by adding it to ignored lines json file')
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
            print('Ignoring line just this time')
            print()
            return False