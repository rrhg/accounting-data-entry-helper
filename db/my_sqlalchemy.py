from datetime import datetime
import pprint

from sqlalchemy.engine import reflection

from rich.console import Console
red = Console(style="red")

from config import client, client_name

from db.models import Base, Client, CkImage, clients_table, ck_img_table
from .my_alembic import add_column_to_client_table
from utils.other import ask_to_continue
from db.session import get_sqlalchemy_session


def _table_has_column(table, column):
    # config = op.get_context().config
    # engine = engine_from_config(
    #     config.get_section(config.config_ini_section), prefix='sqlalchemy.')

    # this was working but not sure if neede to close connection
    # conn_str = fr"sqlite:///{db_file}"
    # engine = create_engine(conn_str)

    with get_sqlalchemy_session() as session:
        engine = session.get_bind()
        insp = reflection.Inspector.from_engine(engine)
        has_column = False
        for col in insp.get_columns(table):
            if column not in col['name']:
                continue
            has_column = True
        session.close()
        return has_column

def only_continue_if_table_has_column(table, column_name):
    if _table_has_column(table, column_name):
        return
    else:
        red.print(f"\n Column '{column_name}' do not exist in db client table.")
        while True:
            a = red.input("Do u want to create it? y / n(quit) : ")
            if a == 'y' or a == 'Y':
                add_column_to_client_table(column_name)
                # return True
                print(f"\n Will stop programm because the column just created, for some reason I couldn't figure out, will not save data until the script is stopped & runned again")
                break
            if a == 'n' or a == 'N':
                break
        print(f"\n Exiting programm. Whether the column was or created or not, need to exit & run the programm again. I spent 3 hours & couldn't figure out why, if we just created the coulmn, it will not savedata on the same run. I tried many wyas found to close the session, the connection, etc, but nothing worked")
        import sys; sys.exit(1)
        # ask_to_continue() # will stop script if user answer n


# maybe create file db/clients.py for the next functions

def get_current_client_id():
    with get_sqlalchemy_session() as session:
        c = session.query(Client).filter(
                Client.name==client_name,
            ).one()
        return c.id


# client_id = get_current_client_id()



def save_value_in_db_client_column(client, column_name, value):
    only_continue_if_table_has_column(clients_table, column_name)
    # print('working,but we stillneed to save the value ')
    _save_value_in_db_client_column(client, column_name, value)

def print_all_clients():
    clients = get_all_clients()
    # clients = get_all_clients_directly_from_sqlite3()
    for c in clients:
        # print(c.name)
        # print(c.id)
        # print(c.created_date)
        # print(f"dir(client): {dir(c)}")
        # print('cks_images:')
        # for i in c.cks_images:
        #     print(f"---> id: {i.id}")
        #     print(f"---> client_id: {i.client_id}")
        #     print(f"---> path: {i.path}")
        #     print(f"---> period: {i.period}")
        #     print(f"---> vendor: {i.vendor}")
        print()
        # print("printing vars(client)")
        pprint.pprint(vars(c))
        print()
        

def create_client(n):
    client = Client(n)
    client.save_to_db()
    # with get_sqlalchemy_session() as session:
    #     client = Client(n)
    #     session.add(client)
    #     session.commit()

def _save_value_in_db_client_column(client, column, value):
    with get_sqlalchemy_session() as session:
        print(f"bf get client, value:{value}")
        client = session.query(Client).filter_by(name=client).one()
        print(f"after get client, value:{value}")
        pprint.pprint(vars(client))
        setattr(client, column, value)
        print(f"after setattr")
        pprint.pprint(vars(client))
        print('==================')
        # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#building-a-relationship
        # parece como si no hubiera q hacer session.add(ck_image)

        session.commit() # this works bc in next run the new cols are there
        session.close()


def get_all_clients():
    with get_sqlalchemy_session() as session:
        return session.query(Client).order_by(Client.id)


def other_query_examples():
    # https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    pass


def create_various():
    """ DO NOT USE - INCOMPLETE
        FOR REFERENCE
    """
    # create catalog
    tshirt, mug, hat, crowbar = (
        Item("SA T-Shirt", 10.99),
        Item("SA Mug", 6.50),
        Item("SA Hat", 8.99),
        Item("MySQL Crowbar", 16.99),
    )
    session.add_all([tshirt, mug, hat, crowbar])
    session.commit()


    # query the order, print items
    order = session.query(Order).filter_by(customer_name="john smith").one()
    print(
        [
            (order_item.item.description, order_item.price)
            for order_item in order.order_items
        ]
    )

    # print customers who bought 'MySQL Crowbar' on sale
    q = session.query(Order).join("order_items", "item")
    q = q.filter(
        and_(Item.description == "MySQL Crowbar", Item.price > OrderItem.price)
    )

    print([order.customer_name for order in q])


def create_initial_tables():
    """
       This is now done with alembic:
           $ alembic revision -m "create original tables"
           $ alembic upgrade head

    # don't use this anymore. For reference only
    conn_str = fr"sqlite:///{db_file}"
    engine = create_engine(conn_str)
    Base.metadata.create_all(engine)
    """
    pass

# if __name__ == "__main__":
#     main()