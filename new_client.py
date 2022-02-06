import shutil 
from os.path import join
from pathlib import Path
from utils.prompt_user_autocomplete import prompt_user_autocomplete
from utils.files import create_dir_w_parents, get_clients_names_from_dir
from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")


"""
    Copy a client(folder recursively) from "client_examples/" to ==> "accounting_clients/" and rename

       Reminder:
        clients == our accounting clients
        partner(type == customers) == customers to our clients
        partner(type == vendors) == vendors to our clients
"""

project = Path(__file__).parent

accounting_clients_folder = join(project,'accounting_clients')
created_clients = get_clients_names_from_dir(accounting_clients_folder)

examples_folder = join(project,'client_examples')
examples = get_clients_names_from_dir(examples_folder)

clients = examples
if created_clients:
    clients = examples + created_clients
red.print( 'Select a client or example to copy : ' )
chosen = prompt_user_autocomplete( ' : ', clients )

print()
while True:
    red.print('Enter new client name : ')
    name = input(' : ')
    if len(name) > 0:
        break

src = ''
if chosen in examples:
    src = join(  examples_folder, chosen)
else:
    src = join(  accounting_clients_folder, chosen)

dest = join( accounting_clients_folder,  name)

created = shutil.copytree(src, dest)

print()
red.print('Created : ')
print(created)
print()