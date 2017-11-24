import pandas as pd
from sqlalchemy import create_engine


class Populate:
    def __init__(self):
        self.engine = create_engine('postgresql://flask:root@localhost:5432/hermes')

    def populate(self):
        products = pd.read_pickle("kijijiphones.pickle")
        products.to_sql('products', con=self.engine, if_exists='append', index=False)

        ebayProducts = pd.read_pickle("ebayProducts.pickle")
        ebayProducts.to_sql('products', con=self.engine, if_exists='append', index=False)

        amazonProducts = pd.read_pickle("amazonProducts.pickle")
        amazonProducts.to_sql('products', con=self.engine, if_exists='append', index=False)

        customers = pd.read_pickle("MOCK_DATA-1.pickle")
        customers.to_sql('customers',con=self.engine, if_exists='append', index=False)

        purchase = pd.read_pickle("purchase.pickle")
        purchase.to_sql('purchases', con=self.engine, if_exists='append', index=False)

populate = Populate()
populate.populate()
