# from rich.console import Console
# red = Console(style="red")
# yellow = Console(style="yellow")


# # TODO : can this be deleted ? Now it was added to file get_transaction_from_line

# def get_transaction_from_ck_line( ck_line ):
#     return

#     amount = client.get_amount_str_from_ck_line( ck_line )
#     amount = try_convert_amount_to_float( amount, ck_line, line=ck_line, caller='utils.vendors.get_or_create_vendor_dict_from_ck_line()' ) # in case the pdf was read incorrectly & the amount includes unrecognized characters, ask to fix it here, instead of getting an error later 
#     amount = str( amount )

#     ck_number = client.get_ck_number_from_ck_line( ck_line )
    
#     date = client.get_date_from_ck_line( ck_line ) 

#     date = try_convert_date( date, ck_line)

#     vendor_key = prompt_user_for_partner_autocomplete(ck_number)

#     if vendor_key == 'create new vendor':
#         vendor_info_dict = create_and_add_partner( '' ) # get info from user. Pass an '' bc is expecting the line(as a string) but in a check we dont have vendor info
#         # vendor_info_dict ===>>>>> {'code': code, 'name': name, 'memo':memo, 'account': account, 'type': vtype, 'strings': strings }
#         vendor_key = vendor_info_dict['code'] 

#     vendors_dict = get_vendors_dict() # get a new one bc we just added a new vendor_key

#     # vendor_key == 'is_a_check' # for testing without entring all checks payees
#     account = vendors_dict[vendor_key]['account']
#     memo = vendors_dict[vendor_key]['description']

#     red.print("\nEnter memo: (Leave Blank to use vendor description) :")
#     new_memo = input(" : ")
#     if new_memo != "": # If user enters something, then use it as memo
#         memo = new_memo 

#     vendor_dict = {
#         'line_has_2_debits': False,
#         'vendor_key': vendor_key,
#         'amount': amount, # this should be a string
#         'ck_number': ck_number,
#         'is_check': True, 
#         'date': date, 
#         'memo': memo, 
#         'account': account,
#         'found': True
#         }
#     return vendor_dict
