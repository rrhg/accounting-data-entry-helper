"""

    This folder(db) was created with $ alembic init db
        - is suppose to be only for alembic revisions (migrations)
        - but added the following files (so the everything related to database is in the same dir)
            - models.py, my_alembic.py, my_sqlalchemy.py, my_sqlite3.py


    Starting from scratch with Alembic
    Instructions:   https://alembic.sqlalchemy.org/en/latest/tutorial.html
        cd /path/to/yourproject
        # if necessary: source /path/to/yourproject/.venv/bin/activate   # assuming a local virtualenv
        to create alembic.ini file + a dir named db for migrations versions & other custome files I putted here like models, slqalchemy warapper, alembic wrapper(custom functions), etc
            $ alembic init db 
        in alembic.ini edit sqlalchemy.url = ...
        in db/env.py add:
            from db.models import Base
            target_metadata = Base.metadata # will generate tables for my models if revision command is run with --autogenerate
        to create initial revision file:
            $ alembic revision --autogenerate -m "create original tables"
        to create 1st migration: (Will also create the sqlite_file.db & the initial tables )
            $ alembic upgrade head


        Next revisions & migrations could be done from cli or programmatically:
            - for dynamically created revisions & migrations
                - see file my_alembic.py
            - for cli
                - edit models(abstraction for tables) in .models file
                - $ alembic revision --autogenerate -m "a msg"
                - or
                - $ alembic revision -m "a msg"
                    - sometimes --autogenerate doesn't work aka doesn't add code in update() & downgrade() functions
                - check the revisions file created
                    - if update() & downgrade() code is correct then run next command
                    - if not then fix code
                - $ alembic upgrade head or $ alembic downgrade

"""    
