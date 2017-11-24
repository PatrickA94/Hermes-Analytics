import pandas as pd
from sqlalchemy import create_engine


class Populate:
    def __init__(self):
        self.engine = create_engine('postgresql://flask:root@localhost:5432/hermes')


    def populate(self):
        # gets players and writes to sql, replacing if table exists
        #products = pd.read_pickle("/home/patsrig/Documents/Databases-project/iphone66.pickle")

        products = pd.read_pickle("kijijiphones.pickle")
        products.to_sql('products', con=self.engine, if_exists='append', index=False)

        '''
        
        YOUR DATA WILL GO HERE AMAZON, EBAY AND TRANSACTION DATA
        
        amazonProducts = pd.read_pickle("amazon.pickle")
        amazonProducts.to_sql('amazonProducts', con=self.engine, if_exists='append', index=False)
        
        ebayProducts = pd.read_pickle("ebayProducts.pickle")
        ebayProducts.to_sql('ebayProducts', con=self.engine, if_exists='append', index=False)
        
        purchase = pd.read_pickle("purchase.pickle")
        purchase.to_sql('purchase', con=self.engine, if_exists='append', index=False)
        
        '''


        #products = pd.read_pickle("/home/patrick/Documents/School/DBproj/Hermes/db/iphone8.pickle")
        #products.to_sql('products', con=self.engine, if_exists='append', index=False)

        customers = pd.read_pickle("MOCK_DATA-1.pickle")
        customers.to_sql('customers',con=self.engine, if_exists='append', index=False)




populate = Populate()
populate.populate()
