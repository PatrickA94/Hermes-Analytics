from flask import Flask, render_template, redirect, jsonify, url_for, request, session, abort
from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, StringField, PasswordField
import db.helper as connection
import pandas as pd
import gmplot
import numpy as np
pd.set_option('display.max_colwidth', -1)

# initalize server
app = Flask(__name__, template_folder='views', static_folder='public')
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# create connection object and get data for teams and players
db = connection.Connection()

# Index page displays the most sold phone for the day, phones under average price for model and the best deal
@app.route('/', methods=['GET', 'POST'])
def index():
    mostsold = db.most_sold24() # might display nothing if there is no data from today
    cheap_phones = db.phones_lta()
    bestdeal = db.bestdeal()

    cheap_phones = db.pandafy(cheap_phones,"MODEL")
    bestdeal = db.pandafy(bestdeal,"MODEL")

    return render_template("index.html", tables=[cheap_phones.to_html(),bestdeal.to_html()],mostsold=mostsold,titles=["","Phones under model average","Best Deals"])

# displays phone under the average price for all phones
@app.route('/phoneavg', methods=['GET', 'POST'])
def phoneavg():
    phone = db.lower_than_global_avg()
    phone = db.pandafy(phone,"MODEL")

    return render_template('trending.html', tables=[phone.to_html()])

# browse through all products in the database
@app.route('/browse', methods=['GET', 'POST'])
def browse():
    allitems = db.allproducts()
    allitems = db.pandafy(allitems,"MODEL")

    return render_template('browse.html', tables=[allitems.to_html()])

# Page for searching items
@app.route('/itemSearch', methods=['GET', 'POST'])
def itemSearch():
    class SelectTeamForm(FlaskForm):
        models = db.get_models()
        memory = db.get_memory_all()
        model = SelectField(choices=models)
        mem = SelectField(coerce=int,choices=memory)

    form = SelectTeamForm()

    print(form.errors)

    # handle post request in form
    if form.validate_on_submit():
        session['MODEL'] = form.model.data
        session['MEMORY'] = form.mem.data
        return redirect('/itemResults')

    return render_template("itemSearch.html", form=form)

# Page that we got to after a itemSearch is submit and valid
@app.route('/itemResults', methods=['GET','POST'])
def results():

    model = session['MODEL']
    memory = session['MEMORY']
    items = db.get_phones(model,memory)
    try:items = db.pandafy(items,"ITEM_ID") # I use try catch here in case the memory for the phone was not valid. Then display what are good values to use
    except:
        propermem= db.get_memory(model)
        return render_template("itemResultsErr.html",tables=[propermem])
    return render_template("itemResults.html", tables=[items.to_html()])

# Page that displays all the users
@app.route('/users', methods=['GET','POST'])
def users():
    users = db.get_users()
    users = db.pandafy(users,"NAME")
    return render_template("users.html", tables=[users.to_html()])

# Page that displays all active users
@app.route('/active', methods=['GET','POST'])
def active():
    users = db.get_active_users()
    try:users = db.pandafy(users,"NAME")
    except: return abort(404)
    return render_template("active.html", tables=[users.to_html()])
# Page displays detailed information about users
@app.route('/detailedUser', methods = ['GET', 'POST'])
def detailedUSer():
    users = db.users_with_transactions()
    users = db.pandafy(users,"NAME")
    return render_template('users.html', tables=[users.to_html()])

# Page that lets us search transactions by email
@app.route('/TransactionSearch', methods=['GET','POST'])
def TransactionSearch():
    class SelectEmailForm(FlaskForm):
         emails = db.get_emails()
         email = SelectField(choices=emails)

    form2 = SelectEmailForm()
    print(form2.errors)

    # handle post request in form
    if form2.validate_on_submit():
        session['EMAIL'] = form2.email.data
        return redirect('/transactionResults')

    return render_template("TransactionSearch.html", form2=form2)

# Page that displays the results of the transaction search page
@app.route('/transactionResults', methods=['GET','POST'])
def transactionResults():

    email = session['EMAIL']
    emails = db.users_trans(email)
    try: emails = db.pandafy(emails,"NAME")
    except: abort(404)
    return render_template("transactionResults.html", tables=[emails.to_html()])

# Displays the best buys and greatest weakly returns
@app.route('/bestBuys', methods=['POST','GET'])
def bestBuys():
    gains = db.biggest_gains()
    gains = db.pandafy(gains,"NAME")

    returns = db.weakly_returns()
    returns = db.pandafy(returns,"NAME")

    return render_template("bestBuys.html", tables= [gains.to_html(),returns.to_html()], titles=['',"Largest profits made","Profit to time ratio, selling faster is better"])

# submit a purchase that a customer has made
@app.route('/PurchaseSubmission', methods = ['POST', 'GET'])
def PurchaseSubmission():
    class PurchaseSub(FlaskForm):
        itemno = db.get_itemno()
        custid = db.get_custID()
        item = SelectField(label='ITEM NUMBER',choices=itemno)
        cust = SelectField(label='CUSTOMER ID',choices=custid)
        price = DecimalField(label='PRICE')
    form = PurchaseSub()

    print(form.errors)

    # handle post request in form and displays a error page if a problem occurs
    if form.validate_on_submit():
        stat = db.cust_buy(form.item.data,form.price.data,int(form.cust.data))
        if stat == 1:
            return render_template("error.html", stat = ["PURCHASE","SUCCESSFUL"])
        else:
            return render_template("error.html", stat = ["PURCHASE",'UNSUCCESSFUL'])
    return render_template('PurchaseSubmission.html', form = form)

#User can submit a sale they have made, only itemno are displayed since they are the KEY
@app.route('/saleSubmission', methods=['POST', 'GET'])
def saleSubmission():
        class saleSub(FlaskForm):
            itemno = db.get_itemno_sell()
            item = SelectField(label='ITEM NUMBER',choices=itemno)
            price = DecimalField(label='PRICE')

        form = saleSub()

        print(form.errors)
        # validates forms and redirects to a error page if there is a problem
        if form.validate_on_submit():
            stat = db.cust_sell(form.item.data,form.price.data)
            if stat == 1:
                return render_template("error.html", stat = ["SALE","SUCCESSFUL"])
            else:
                return render_template("error.html", stat = ["SALE",'UNSUCCESSFUL'])
        return render_template('saleSubmission.html', form = form)

# counts how many models are bought but not sold yet
@app.route('/modelsPurchased', methods=['POST', 'GET'])
def modelsPurchased():
    purch = db.purchased()
    purch = db.pandafy(purch,"MODEL")

    return render_template('modelsPurchased.html', data=[purch.to_html()])

# displays models that have not been bought by anyone yet
@app.route('/unboughtModels', methods=['POST', 'GET'])
def unboughtModels():
    notpurch = db.unbought_models()
    notpurch = db.pandafy(notpurch,"MODEL")

    return render_template('unboughtModels.html', data= [notpurch.to_html()])

# displays a heatmap of where the products are
@app.route('/heatmap', methods=['POST', 'GET'])
def heatmap():

    coridinate = db.get_coridinate()
    cord = np.asarray(coridinate,dtype=float)

    gmap = gmplot.GoogleMapPlotter.from_geocode("Toronto",7)
    gmap.heatmap(cord[:,0],cord[:,1],radius=20, threshold=10, opacity=0.8, dissipating=True)
    gmap.draw('views/mymap.html')

    return render_template("mymap.html")

# Page for adding customers to the database
@app.route('/addCust', methods=['POST', 'GET'])
def addCust():
    class Customer(FlaskForm):
            cust_id = StringField()
            name = StringField()
            password = PasswordField()
            email = StringField()
            city = StringField()
            street = StringField()
            postal = StringField()
    form = Customer()

    print(form.errors)
    # Checks if form is ok and goes to error page if there is a problem
    if form.validate_on_submit():
        stat = db.addCust(form.cust_id.data,form.name.data,form.password.data,form.email.data,form.city.data,form.street.data,form.postal.data)
        if stat == 1:
            return render_template("error.html", stat = ["NEW USER","SUCCESSFUL"])
        else:
            return render_template("error.html", stat = ["NEW USER",'UNSUCCESSFUL'])
    return render_template('newUser.html', form = form)

# API for getting all phones of a desired model
@app.route('/api/get_phones/<model>', methods=['GET'])
def get_phones(model):
    phones = db.get_phones_api(model)
    return jsonify(phones)
# REST api for creating a new user in the database,
@app.route('/api/addItem', methods=['POST'])
def create_user():

    if not request.json or not 'ITEM_ID' in request.json:
        abort(400)
    item = {
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

    stat = db.addItem(item['item_id'],item['platform'],item['carrier'],item['model'],item['memory'],item['latitude'],
                      item['longitude'],item['address'],item['description'],item['poster_id'],item['price'],item['title'],item['url'],item['visits'],item['shipping'])
    if stat == 1:
        return jsonify({'item': item}), 201
    else:
        return jsonify({'item': item}), 404



if __name__ == '__main__':
    app.run(debug=False, host='localhost')
