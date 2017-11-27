BEGIN;
--
-- Create model customers
--
CREATE TABLE "customers" 
("CUST_ID" varchar(30) NOT NULL PRIMARY KEY, 
"DATE_JOINED" date NOT NULL, 
"NAME" varchar(50) NOT NULL, 
"PASS" varchar(30) NOT NULL, 
"EMAIL" varchar(254) NOT NULL, 
"CITY" varchar(30) NOT NULL, 
"STREET" varchar(50) NOT NULL, 
"POSTAL" varchar(15) NULL);
--
-- Create model products
--
CREATE TABLE "products" 
("ITEM_ID" varchar(50) NOT NULL PRIMARY KEY,
"DATE_POSTED" timestamp with time zone NULL,
"PLATFORM" varchar(20) NOT NULL,
"CARRIER" varchar(20) NOT NULL,
"MODEL" varchar(60) NOT NULL,
"MEMORY" smallint NULL,
"LATITUDE" numeric(9, 3) NULL,
"LONGITUDE" numeric(9, 3) NULL,
"ADDRESS" text NULL,
"DESCRIPTION" text NULL,
"POSTER_ID" varchar(60) NULL,
"PRICE" numeric(10, 2) NOT NULL,
"TITLE" text NOT NULL,
"URL" varchar(200) NOT  NULL,
"VISITS" smallint NULL,
"SHIPPING" numeric(10, 2) NULL);
--
-- Create model purchases
--
CREATE TABLE "purchases" 
("TRANS_ID" serial NOT NULL PRIMARY KEY, 
"SALE_AMOUNT" numeric(10, 2) NULL,
"DATE_SOLD" timestamp with time zone NULL,
"PURCHASE_AMOUNT" numeric(10, 2) NOT NULL,
"DATE_BOUGHT" timestamp with time zone NOT NULL, 
"SHIPPING" numeric(10, 2) NULL,
"CUST_ID" varchar(30) NOT NULL, 
"ITEM_ID" varchar(30) NOT NULL);

CREATE INDEX "customers_CUST_ID_2a3ee316_like" ON "customers" ("CUST_ID" varchar_pattern_ops);
CREATE INDEX "products_ITEM_ID_017f8646_like" ON "products" ("ITEM_ID" varchar_pattern_ops);
ALTER TABLE "purchases" ADD CONSTRAINT "purchases_CUST_ID_6aec3a9f_fk_customers_CUST_ID" FOREIGN KEY ("CUST_ID") REFERENCES "customers" ("CUST_ID") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "purchases" ADD CONSTRAINT "purchases_ITEM_ID_f31bf070_fk_products_ITEM_ID" FOREIGN KEY ("ITEM_ID") REFERENCES "products" ("ITEM_ID") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "purchases_CUST_ID_6aec3a9f" ON "purchases" ("CUST_ID");
CREATE INDEX "purchases_CUST_ID_6aec3a9f_like" ON "purchases" ("CUST_ID" varchar_pattern_ops);
CREATE INDEX "purchases_ITEM_ID_f31bf070" ON "purchases" ("ITEM_ID");
CREATE INDEX "purchases_ITEM_ID_f31bf070_like" ON "purchases" ("ITEM_ID" varchar_pattern_ops);
ALTER SEQUENCE "purchases_TRANS_ID_seq" RESTART WITH 100;
COMMIT;
