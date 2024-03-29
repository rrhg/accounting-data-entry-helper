import re, fileinput
from alembic import op, command
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import Session
from alembic import context

import alembic
from alembic.config import Config
import sqlalchemy as sa
from db.models import clients_table
from utils.suppress_io import capture_stdout
from utils.other import ask_to_continue
from settings import db_file


alembic_ini_file_path = r"C:\Users\r\OneDrive - H&J Accounting\Documents\Ricky\accounting-data-entry-helper\alembic.ini"


# from sqlalchemy import inspect

# def column_exists(table_name, column_name):
#     bind = op.get_context().bind
#     insp = inspect(bind)
#     columns = insp.get_columns(table_name)
#     return any(c["name"] == column_name for c in columns)


def add_column_to_client_table(column_name):
    add_text_column_code_to_model_code(column_name)

    alembic_cfg = Config(alembic_ini_file_path)

    conn_str = fr"sqlite:///{db_file}"
    engine = create_engine(conn_str, poolclass=NullPool)
    session = Session(engine)
    with engine.connect() as connection:
    # with connectable.connect() as connection:
        alembic_cfg.attributes['connection'] = connection

        revision_file = run_revision_command_and_get_file(alembic_cfg, column_name)
        add_text_column_code_to_revision_file(revision_file, column_name) # bc command revision autogenerate=True did not gave me reliable results (did not always created code) 
        command.upgrade(alembic_cfg, "head")  # aka $ alembic upgrade head aka migrate(Django)
        session.commit()
        session.close()
        connection.close()
    # conn = op.get_bind() # error no attr
    # conn = alembic.context.get_bind()
    # engine = engine_from_config(alembic_cfg)
    # conn = engine.connection
    # conn.close()
    # session = sa.orm.Session(bind=op.get_bind())
    # session.close()


def add_text_column_code_to_revision_file(file_path, column_name):
    indent = "    "
    end = "\n"
    upgrade_code = (
          indent
        + f"op.add_column('{clients_table}', sa.Column('{column_name}', sa.String()))"
        + end
    )
    downgrade_code = (
          indent
        + f"op.drop_column('{clients_table}', '{column_name}')"
        + end
    )

    previous_line = ''
    for line in fileinput.FileInput(file_path,inplace=1):
        if "upgrade" in previous_line:
            line=line.replace(line, upgrade_code)
        elif "downgrade" in previous_line:
            line=line.replace(line, downgrade_code)

        print(line, end="") # this magically is written to the file
        previous_line = line


def add_text_column_code_to_model_code( column_name):
    models_file = r"C:\Users\r\OneDrive - H&J Accounting\Documents\Ricky\accounting-data-entry-helper\db\models.py"
    code = f"{column_name} = Column(String())"
    indent = "    "
    end = "\n"
    code_line = indent + code + end
    marker_line = ''
    for line in fileinput.FileInput(models_file,inplace=1):
        if "# add autogenerated column to Client here" in line:
            marker_line = line
            line=line.replace(line, code_line )
            print(line, end="") # this magically is written to the file
            print()
            print(marker_line, end="") # keep it for next added column
        else:
            print(line, end="")

        previous_line = line


def run_revision_command_and_get_file(alembic_cfg, column_name):
    """ Returns file path (python file with revision(migration) for execute when run command.update(... or using he cli $ alembic update head"""
    msg = f"add column {column_name} to table client"

    def run_revision_command():
        # no autogenerate bc is not reliable. Sometimes doesn't work
        command.revision(alembic_cfg, message = msg) # aka $ alembic revision --autogenerate -m "create original tables"
        # command.revision(alembic_cfg, message = msg, autogenerate=True) # aka $ alembic revision --autogenerate -m "create original tables"

    stdout = capture_stdout(run_revision_command)

    # find file path in stdout
    file = re.findall(r"(C:.*\.py)", stdout)
    # print(f"=={file[0]}==")
    return(file[0])


# def update_aka_migrate():
#     # revision version python file must have already been created
#     #create new config so it will load the models file again with the changes(added column)
#     from alembic.config import Config
#     from alembic import command
#     ini_path = r"C:\Users\r\OneDrive - H&J Accounting\Documents\Ricky\accounting-data-entry-helper\alembic.ini"
#     alembic_cfg = Config(ini_path)
#     # msg = f"add column {column_name} to table client"

#     # command.revision(alembic_cfg, message = msg, autogenerate=True) # aka $ alembic revision --autogenerate -m "create original tables"
#     command.upgrade(alembic_cfg, "head")  # aka $ alembic upgrade head
#     # a = input('continue ?')
