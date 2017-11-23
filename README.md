# HermesV2
Project repository with setup and usage instructions

# TODO

- Make sure we have all required VIEWS/QUERIES
- Styling for webpages
- Fake data for transactins
- Make API with JSON output

# Setup
- [Linux](#linux-setup)
- [Pycharm Setup](#pycharm-ide-setup)
- [Running Project](#run-project)



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

### PostgreSQL Database Setup
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

Run the python script called dbint.py in DB/schema/ directory, this will create the tables in the database.
Then run the populate.py script to populate the database with the initial data

### Flask Server Setup

Run the web.py file, this will initilize the web server.
Navigate to http://localhost:5000



# Run Project
- use configurations created in PyCharm for `web.py` and `populate.py`
- to run, click the green arrow button besides the dropdown used for configuration


**Note:** You can run the web and populate scripts on the command line if you ran the package installation on db.


