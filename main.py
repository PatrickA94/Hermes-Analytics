from db.schema import dbinit
from db import populate
from files import itemdict

# used to set up database
if __name__ == "__main__":
    dbinit.main('db/schema/proj.sql')
    populate.main(itemdict)
