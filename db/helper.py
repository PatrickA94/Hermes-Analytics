import psycopg2
import datetime
import simplejson
import pandas as pd
from psycopg2.extras import RealDictCursor


class Connection:
    def __init__(self):
        con = psycopg2.connect(database='hermes', user='flask', host='localhost', password='root')
        self.cur = con.cursor()
        self.dict = con.cursor(cursor_factory = RealDictCursor)
        self.commit = con.commit
        self.roll = con.rollback

    # HELPER QUERIES

    def get_emails(self):
        self.cur.execute('select "EMAIL","EMAIL" from customers order by "EMAIL" ASC')
        return self.cur.fetchall()

    def get_models(self):
        self.cur.execute('select Distinct "MODEL","MODEL" from products ')
        return self.cur.fetchall()

    def get_itemno(self):
        self.cur.execute(' select "ITEM_ID","ITEM_ID" from products')
        return self.cur.fetchall()

    def get_itemno_sell(self):
        self.cur.execute('select "ITEM_ID", "ITEM_ID" from purchases where "SALE_AMOUNT" is NULL ')
        return self.cur.fetchall()

    def get_custID(self):
        self.cur.execute('select "CUST_ID","NAME" from customers')
        return self.cur.fetchall()

    def get_memory_all(self):
        self.cur.execute('select distinct "MEMORY","MEMORY" from products where "MEMORY" is NOT NULL' )
        return self.cur.fetchall()

    def get_memory(self,model):
        self.cur.execute('select distinct "MEMORY" from products where "MEMORY" is NOT NULL and "MODEL"= %s;',(model,) )
        return self.cur.fetchall()

    def get_users(self):
        self.dict.execute('select "NAME", "EMAIL" from customers')
        return self.dict.fetchall()

    def allproducts(self):
        self.dict.execute('select "ITEM_ID","PLATFORM","CARRIER", "MODEL", "MEMORY","PRICE","TITLE","URL" from products order by "DATE_POSTED"')
        return self.dict.fetchall()

    def get_lat(self):
        self.cur.execute('select "LATITUDE","LONGITUDE" from products where "LATITUDE" is NOT NULL')
        return self.cur.fetchall()

    def get_long(self):
        self.cur.execute('select "LONGITUDE" from products where "LONGITUDE" is NOT NULL')
        return self.cur.fetchall()


    # TRENDING and ANALYTICS

    def most_sold24(self):
        now = datetime.datetime.today()
        self.cur.execute('select "MODEL" from products where extract(day from "DATE_POSTED") = %s;',(now.day,))
        return self.cur.fetchone()

    #	Select all models whose price is less than the global purchase average CORRELATED SUBQUERY 3
    def lower_than_global_avg(self):
        self.dict.execute('SELECT p."MODEL", p."PRICE", p."URL" '
                        'FROM PRODUCTS AS p '
                        'WHERE p."PRICE" < (SELECT AVG(t."PURCHASE_AMOUNT") FROM purchases AS t WHERE p."ITEM_ID"= t."ITEM_ID")')
        return self.dict.fetchall()

    def phones_lta(self):
        self.dict.execute('select products."MODEL",products."PRICE",products."TITLE", products."TITLE", products."CARRIER", products."PLATFORM" '
                         'from products '
                         'INNER JOIN (select "MODEL", avg("PRICE") as "PRICE" '
                                    'from products '
                                    'group by "MODEL") as phoneav '
                         'on products."MODEL"=phoneav."MODEL"'
                         'where products."PRICE"< phoneav."PRICE"')
        return self.dict.fetchall()
    def bestdeal(self):
        self.dict.execute('select products."MODEL",products."PRICE",products."TITLE",products."MEMORY",(products."PRICE"-phoneav."PRICE") as dif '
                         'from products '
                         'INNER JOIN (select "MODEL", avg("PRICE") as "PRICE" '
                                    'from products '
                                    'group by "MODEL") as phoneav '
                         'on products."MODEL"=phoneav."MODEL"'
                         'where products."PRICE"< phoneav."PRICE"'
                         'order by dif')
        return self.dict.fetchall()


    def get_phones(self,model_type,memory):
        self.dict.execute('select "ITEM_ID","PLATFORM","CARRIER", "MODEL", "MEMORY","PRICE","TITLE","URL" from products where "MODEL"=%s and "MEMORY"=%s', [model_type,memory])
        return self.dict.fetchall()


    def cust_buy(self,item_id,amount,cust_id):
        sql = 'insert into purchases ("PURCHASE_AMOUNT","DATE_BOUGHT","CUST_ID","ITEM_ID") values (%s,current_timestamp,%s,%s)'
        try:
            self.cur.execute(sql,[amount,cust_id,item_id])
            self.commit()
            return 1
        except:
            self.roll()
            return 0


    def cust_sell(self,item_id,amount):
        sql = 'update purchases set "SALE_AMOUNT"= %s, "DATE_SOLD"=current_timestamp where "ITEM_ID"=%s'
        try:
            self.cur.execute(sql,[amount,item_id])
            self.commit()
            return 1
        except:
            self.roll()
            return 0


#	Improve this by linking more tables and getting more information
    def get_active_users(self):
        self.dict.execute('select "NAME","EMAIL" '
                         'from customers, purchases '
                         'where purchases."CUST_ID" = customers."CUST_ID"')
        return self.dict.fetchall()

    def users_trans2(self,email):
        self.dict.execute('select "SALE_AMOUNT","DATE_SOLD","PURCHASE_AMOUNT","DATE_BOUGHT","SHIPPING","NAME" '
                         'from customers, purchases '
                         'where purchases."CUST_ID"=customers."CUST_ID" and purchases."CUST_ID"= ( '
                            'select "CUST_ID" '
                            'from customers  '
                            'where "EMAIL" = %s)',[email])
        return self.dict.fetchall()

#	THIS SHOWS ALL USERS WITH THEIR ASSOCIATED PURCHASES for FULL JOIN view

    def users_with_transactions(self):
        self.dict.execute('SELECT customers."NAME","PURCHASE_AMOUNT", "SALE_AMOUNT" , purchases."TRANS_ID" '
        'FROM customers FULL OUTER JOIN purchases ON customers."CUST_ID" = purchases."CUST_ID"')
        return self.dict.fetchall()
# this shows all the models that havent been bought yet for UNION EXCEPT or INTERSECT view 

    def unbought_models(self):
        self.dict.execute('SELECT products."MODEL" FROM products '
            'EXCEPT(SELECT products."MODEL" FROM products , purchases WHERE products."ITEM_ID" = purchases."ITEM_ID")')
        return self.dict.fetchall()


    def users_trans(self,email):
        self.dict.execute('select "SALE_AMOUNT","DATE_SOLD","PURCHASE_AMOUNT","DATE_BOUGHT",products."SHIPPING","NAME","PLATFORM", "MODEL" '
                         'from customers '
                          'INNER JOIN purchases on customers."CUST_ID" = purchases."CUST_ID" '
                          'INNER JOIN products on purchases."ITEM_ID" = products."ITEM_ID" '
                         'where purchases."CUST_ID"= ( '
                            'select "CUST_ID" '
                            'from customers  '
                            'where "EMAIL" = %s)',[email])
        return self.dict.fetchall()


# VIEW 1 : Covers 3 tables
    def biggest_gains(self):
        self.dict.execute('select "NAME","MEMORY", "MODEL","PLATFORM",("SALE_AMOUNT"-"PURCHASE_AMOUNT") as profit '
                         'from purchases, products,customers '
                         'where "SALE_AMOUNT" is NOT NULL and purchases."ITEM_ID"=products."ITEM_ID" and purchases."CUST_ID"=customers."CUST_ID" '
                         'order by profit DESC ')
        return self.dict.fetchall()
# Show which product it was 
    def weakly_returns(self):
        self.dict.execute('select "PLATFORM","MEMORY","NAME", "MODEL", hot.gain '
                         'from purchases '
                         'INNER JOIN (select "ITEM_ID",("SALE_AMOUNT"-"PURCHASE_AMOUNT")/nullif(extract(day from "DATE_SOLD"-"DATE_BOUGHT")/(7),0.0) as gain '
                            'from purchases where "SALE_AMOUNT" is NOT NULL order by gain DESC) as hot '
                         'ON purchases."ITEM_ID"=hot."ITEM_ID" '
                        'INNER JOIN products on products."ITEM_ID"=purchases."ITEM_ID" '
                        'INNER JOIN customers on customers."CUST_ID"=purchases."CUST_ID"  '
                         'ORDER by hot.gain DESC')
        return self.dict.fetchall()

# VIEW 2 : NESTED query with ANY/ALL and group by
    def purchased(self):
        self.dict.execute(' select "MODEL",count("MODEL") from products '
                          'where "ITEM_ID" = ANY '
                          '( select "ITEM_ID" '
                          'from purchases '
                          'where "SALE_AMOUNT" is NULL) '
                          'group by "MODEL";')
        return self.dict.fetchall()

    def myconverter(self,o):
        if isinstance(o, datetime.datetime):
            return o.__str__()


    def pandafy(self,data,index):
        pdata = simplejson.dumps(data, default=self.myconverter)
        pdata = pd.read_json(pdata)
        pdata.set_index([index],inplace=True)
        pdata.index.name=None
        return pdata


