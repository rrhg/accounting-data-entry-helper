from .get_sub_directories import get_sub_directories


def get_clients_names_from_dir(dir_path):
    clients = []
    sub_dirs = get_sub_directories( dir_path )
    
    for d in sub_dirs:
        if d != '__pycache__':
            clients.append( d )

    return clients
 