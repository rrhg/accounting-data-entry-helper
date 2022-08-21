import sqlite3
from settings import db_file

"""     !  DO NOT USE        !
           ----------
           
    NOW WE ARE USING my_alembic.py & my_sqlalchemy.py
    But do not delete, may be used for reference
"""

"""
    Some sqlite3 helper functions
    Customized for a 1 table db where all columns will be text
    Warning: Interpollating values using f"{}" is insecure. But this is a local db that will not have access to the internet
"""


def get_all_clients_directly_from_sqlite3():
    """ DO NOT USE
        NOW WE R USING SQLALCHEMY & ALEMBIC
    """
    import sqlite3
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    sql_command = (f"SELECT * FROM {clients_table}")
    # sql_command = (f"SELECT * FROM {clients_table} WHERE name = {name}")

    r = cursor.execute(sql_command)
    connection.commit()
    connection.close()
    return r

def add_text_column_to_clients(column_name): # https://stackoverflow.com/questions/7300948/add-column-to-sqlalchemy-table
    """ DO NOT USE
        NOW WE R USING SQLALCHEMY & ALEMBIC
    """
    import sqlite3
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    sql_command = (f"ALTER TABLE {clients_table} ADD COLUMN {column_name} TEXT")
    # base_command = (f"ALTER TABLE '{clients_table}' ADD column '{column_name}' TEXT")
    # sql_command = base_command.format(table_name=table_name, column_name=column_name, data_type=data_type_formatted)

    cursor.execute(sql_command)
    connection.commit()
    connection.close()


table = 'clients'
col_type = 'text' # all values will be text(strings)

def add_blob_column(name):
    with Connection() as c:
        c.execute(f"alter table {table} add column '{name}' 'blob'")

def add_column(col_name):
    with Connection() as c:
        c.execute(f"alter table {table} add column '{col_name}' '{col_type}'")
        # c.execute(f"alter table {table} add column (? ?)", (col_name, col_type ))

def get_row(client):
    with Connection() as c:
        return c.execute(f"SELECT * FROM {table} WHERE client = (?)", (client,)).fetchone()
        # use: row['client']  or row['cks_imgs_period']  

def get_all():
    with Connection() as c:
        return c.execute(f"SELECT * FROM {table}").fetchall()
        # use: row['client']  or row['cks_imgs_period']  


def add_client_insert_row(client):
    with Connection() as c:
        c.execute(f"INSERT INTO {table} (client) VALUES (?)", (client,)) # other columns will be null

def delete_client_row(client):
    with Connection() as c:
        c.execute(f"DELETE from {table} WHERE client = (?)", (client,))

def insert_to_1_column(client, column, value ):
    with Connection() as c:
        c.execute(f'UPDATE {table} SET {column}={value} WHERE client="{client}"')
        # c.execute(f"UPDATE {table} SET cks_imgs_period='2022-05' WHERE client='vida'")

def create_table():
    with Connection() as c:
        c.execute(f"CREATE TABLE {table} (client text, cks_imgs_period text)")
                #    (client text, mail_address text, symbol text, qty real, price real)''')

def get_column_count():
    with Connection() as c:
        first_row = c.execute(f"SELECT * FROM {table} ORDER BY ROWID ASC LIMIT 1").fetchone()
        return len(first_row)


class Connection():   # https://stackoverflow.com/questions/19522505/using-sqlite3-in-python-with-with-keyword
    def __init__(self, file=db_file):
        self.file=file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row  # return 'dictionary' rows after fetchall or fetchone instead of tupples
        return self.conn
        # return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()