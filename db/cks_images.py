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


def get_current_client_id():
    with get_sqlalchemy_session() as session:
        c = session.query(Client).filter(
                Client.name==client_name,
            ).one()
        return c.id


client_id = get_current_client_id()


def create_ck_image(path, period, client_name):
    with get_sqlalchemy_session() as session:
        client = session.query(Client).filter_by(name=client_name).one()
        client.cks_images.append(CkImage(path, period))

        # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#building-a-relationship
        # parece como si no hubiera q hacer session.add(ck_image)

        session.commit()


def get_all_cks_images():
    with get_sqlalchemy_session() as session:
        return session.query(CkImage).order_by(CkImage.period)


def get_infered_payee_from_ck_image(ck_number):
    with get_sqlalchemy_session() as session:
        l = session.query(CkImage).filter(
            CkImage.ck_number==ck_number,
            CkImage.client_id == client_id, 
            ).all()
        
        if len(l) > 1:
            print(f"\n Found more than 1 ck_image with number: {ck_number} in def get_infered_payee_from_ck_image() ")
            ask_to_continue()
        if l:
            img = l[0]
            return img.payee_txt_hugginface,
        else:
            return f"Did not found ck# {ck_number} in cks images for this client"

def show_ck_image_by_ck_number(ck_number):
    with get_sqlalchemy_session() as session:
        # return session.query(CkImage).filter(CkImage.ck_number==ck_number).one_or_none() # error if more than one
        l = session.query(CkImage).filter(
            CkImage.ck_number==ck_number,
            CkImage.client_id == client_id, 
            ).all()
        
        if len(l) > 1:
            print(f"\n Found more than 1 ck_image with number: {ck_number}")
            ask_to_continue()
        found = True if l else False
        img = l[0]
        img.show_ck_img()
        return (found,
                img.payee_txt_hugginface,
                img.payee_txt_textract,
        )

# def show_ck_image_if_ck_number(ck_number):
#     with get_sqlalchemy_session() as session:
#         img = session.query(CkImage).filter(CkImage.ck_number==ck_number).one_or_none()
#         if img:
#             img.show_ck_img()
#             return True
#         else:
#             return False



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# ME QUEDE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# PONER EN get_or_create_vendor_dict_from_ck_line
# UNA VEZ SEPA CUAL ES EL VENDOR
def save_payee_img_in_vendor_dir(dir, vendor,ck_number):
    with get_sqlalchemy_session() as session:
        l = session.query(CkImage).filter(
            CkImage.ck_number==ck_number,
            CkImage.client_id == client_id, 
            ).all()

        if len(l) > 1:
            print(f"\n Found more than 1 ck_image with number: {ck_number}")
            ask_to_continue()
        if l:
            img = l[0]
            img.save_payee_img_in_dir(dir, vendor)


def this_period_cks_images_done(period):
    with get_sqlalchemy_session() as session:
        q = session.query(CkImage).filter(CkImage.period==period).all()
        return bool(q) 


def get_cks_imgs_numbers_for_period(period):
    with get_sqlalchemy_session() as session:
        l = []
        q = session.query(CkImage).filter(CkImage.period==period)
        return [c.ck_number for c in q]


def other_query_examples():
    # https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    pass

def print_all_cks_images():
    images = get_all_cks_images()
    # clients = get_all_clients_directly_from_sqlite3()
    for i in images:
        print()
        print(i.ck_number)
        # print(i.id)
        # print(i.created_date)
        # print(f"dir(client): {dir(i)}")
        # print('cks_images:')
        # print("printing vars(client)")
        # pprint.pprint(vars(i))
        print()


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