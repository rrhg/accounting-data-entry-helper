import shutil 
from os.path import join
from pathlib import Path
from utils.prompt_user_autocomplete import prompt_user_autocomplete
from utils.files import create_dir_w_parents, get_clients_names_from_dir

"""
    Copy a client(folder recursively) from 
    client_examples/ to ==> accounting_clients/
    and rename
"""

project = Path(__file__).parent

""" clients == our accounting clients; customers==customers to our clients; definition of client == seek professional services, longer business relashionship """
clients_folder = join(project,'accounting_clients')
examples_folder = join(project,'client_examples')
# TODO inlude old clients in /accounting_clients folder
examples = get_clients_names_from_dir(examples_folder)
example = prompt_user_autocomplete( 'Select an example to copy : ', examples )

print()
while True:
    name = input('Enter new client name : ')
    if len(name) > 0:
        break

src = join(  examples_folder, example)
dest = join( clients_folder,  name)

created = shutil.copytree(src, dest)

print()
print ('Created ==> ')
print(created)
print()