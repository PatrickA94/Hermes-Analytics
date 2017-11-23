# HermesV2
Project repository with setup and usage instructions

# Setup
- [Linux](#linux-setup)
- [Pycharm Setup](#pycharm-ide-setup)
- [Running Project](#run-project)
- [Additional Styling](#styling)
- [Tasks to Complete For Lab](#complete)


- Install [PostgreSQL](https://www.postgresql.org/download/windows/)
- Install [pgAdmin3](https://www.pgadmin.org/download/windows.php)


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
createuser root
createdb hermes -O root
psql
\password root
password: root
enter it again: root
\q
exit
```


# PyCharm IDE Setup
- download and install [PyCharm](https://www.jetbrains.com/pycharm/)
- you can get a free license from JetBrains if you are a [student](https://www.jetbrains.com/student/)
- to add your venv as an interpreter follow these [instructions](https://www.jetbrains.com/help/pycharm/2016.1/adding-existing-virtual-environment.html)

![VENV Interpreter Setup](img/pycharm-venv.png)

### PyCharm Debugging
- click on the dropdown arrow ![Arrow](img/arrow.png) and select edit configurations
- add a python configuration with the following settings

**For Web Server**
![Configuration Setup Web](img/web-config.png)

**For Databse Population**
![Configuration Setup Web](img/populate-config.png)

# Run Project
- use configurations created in PyCharm for `web.py` and `populate.py`
- to run, click the green arrow button besides the dropdown used for configuration

![Run](img/run.png)

- to debug, click on the green sun icon

![Debug](img/debug.png)

**Note:** You can run the web and populate scripts on the command line if you ran the package installation on db.

# Styling
- I used Materialize.css for this project


