"""    Reminder:
        clients == our accounting clients
        partner(type == customers) == customers to our clients
        partner(type == vendors) == vendors to our clients
"""


# partner_dict = {'code': '', 'name': '', 'memo':'',
#  'account': '', 'type': '', 'strings': [] }
partner_dict = {
        'code': '',
        'name': '',
        'memo':'',
        'description': '',
        'account': '', # backward compatible
        'account_can_change': False,
        'type': '',
        'strings': [],
        'affects_more_than_1_account': False,
        'accounts': [],
        'split_amount_in_half': False,
    }



