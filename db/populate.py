import pandas as pd
from sqlalchemy import create_engine


class Populate:
    # start the connection to the database
    def __init__(self):
        self.engine = create_engine('postgresql://flask:root@localhost:5432/hermes')
    # fill the database with all the data we scraped and genrated
    def populate(self, itemdict):
        products = pd.read_pickle(itemdict['kijiji'])
        products.to_sql('products', con=self.engine, if_exists='append', index=False)

        ebayProducts = pd.read_pickle(itemdict['ebay'])
        ebayProducts.to_sql('products', con=self.engine, if_exists='append', index=False)

        amazonProducts = pd.read_pickle(itemdict['amazon'])
        amazonProducts.to_sql('products', con=self.engine, if_exists='append', index=False)

        customers = pd.read_pickle(itemdict['customers'])
        customers.to_sql('customers',con=self.engine, if_exists='append', index=False)

        purchase = pd.read_pickle(itemdict['purchases'])
        purchase.to_sql('purchases', con=self.engine, if_exists='append', index=False)

def main(item):
    populate = Populate()
    populate.populate(item)
