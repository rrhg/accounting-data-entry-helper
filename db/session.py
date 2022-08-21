from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool
from settings import db_file


connection_str = fr"sqlite:///{db_file}"


def get_sqlalchemy_session():
    engine = create_engine(connection_str, poolclass=NullPool)# do not pool (share connection) bc sometimes 
    session = Session(engine)
    return session

    # engine = create_engine("sqlite://") # original
    # engine = create_engine(r'sqlite:///C:\path\to\foo.db') # https://stackoverflow.com/questions/19260067/sqlalchemy-engine-absolute-path-url-in-windows
    # engine = session.get_bind()
    # insp = reflection.Inspector.from_engine(engine)