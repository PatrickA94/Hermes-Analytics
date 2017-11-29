# HermesV2
Project repository with setup and usage instructions


# Setup
- [Linux](#linux-setup)
- [Pycharm Setup](#pycharm-ide-setup)
- Install [PostgreSQL](https://www.postgresql.org/download/windows/)


# Linux Setup
- Install git if not already installed
```
sudo apt-get install git

sudo apt install python-pip python-dev build-essential libpq-dev
sudo apt-get install postgresql pgadmin3
sudo pip install virtualenv virtualenvwrapper
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py build
python setup.py install
deactivate
```

## PostgreSQL Database Setup
- run these commands in terminal
```
sudo su postgres
createuser flask
createdb hermes 
psql
\password flask
password: root
enter it again: root
grant all privileges on database hermes to flask;
\q
exit
```
Before running the script below, ensure you are in the virtual enviroment and in heremesv2 directory
```
python main.py
```


## Flask Server Setup

Run the web.py file, this will initilize the web server.
Navigate to http://localhost:5000

## API Documentation
To grab a json of all phones of a certain model use:
```
http://localhost:5000/api/get_phones/<model>
```
Where `<model>` gets replaced with a phone model i.e. (iphone6, samsungs8, iphonex....)
  
To add a new phone to the database use:
```
http://localhost:5000/api/addItem
```
The body of the request should be a json with the layout below:
```
{
        'item_id': request.json['ITEM_ID'],
        'platform': request.json['PLATFORM'],
        'carrier': request.json['CARRIER'],
        'model': request.json['MODEL'],
        'memory': request.json.get('MEMORY',None),
        'latitude': request.json.get("LATITUDE",None),
        'longitude': request.json.get('LONGITUDE',None),
        'address': request.json.get('ADDRESS',None),
        'description': request.json.get('DESCRIPTION',None),
        'poster_id': request.json.get('POSTER_ID',None),
        'price': request.json['PRICE'],
        'title': request.json['TITLE'],
        'url': request.json['URL'],
        'visits': request.json.get('VISITS', None),
        'shipping': request.json.get('SHIPPING',None)
}
```
# Web Scrapers
They are here for reference they are not integrated into our project, but used to get data and populate the database
### Kijiji Scraper
To run the kijiji scraper run this in terminal to get the usage instructions and values to pass
```
python kijiji-scraper.py -h
```
The output file requires cleaning after since kijiji is filled with ads so run to get the usage instructions and values to pass
```
python adscrubber.py -h
```
### Amazon Scraper
To run the scraper either run it in your IDE of choice or run ./amazon_scraper_v3.py in terminal(note that you have to be in the same directory the file is in). A json file with the data will be created in the same directory as the script.
### eBay Scraper
  


