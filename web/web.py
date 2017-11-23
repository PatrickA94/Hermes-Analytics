from flask import Flask, render_template, redirect, jsonify, url_for, request, session, abort
from flask_restful import Api
from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import SelectField
import db.helper as connection
import pandas as pd
pd.set_option('display.max_colwidth', -1)

# initalize server
app = Flask(__name__, template_folder='views', static_folder='public')
api = Api(app)
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
CsrfProtect(app)


# create connection object and get data for teams and players
db = connection.Connection()

# Index page displays the mostold phone for the day, phones under average price for model and the best deal
@app.route('/', methods=['GET', 'POST'])
def index():
    mostsold = db.most_sold24() # might display nothing if there is no data from today
    cheap_phones = db.phones_lta()
    bestdeal = db.bestdeal()

    cheap_phones = db.pandafy(cheap_phones,"MODEL")
    bestdeal = db.pandafy(bestdeal,"MODEL")

    return render_template("index.html", tables=[cheap_phones.to_html(),bestdeal.to_html()],mostsold=mostsold)

# Page for searching items
@app.route('/itemSearch', methods=['GET', 'POST'])
def itemSearch():
    class SelectTeamForm(FlaskForm):
        models = db.get_models()
        memory = db.get_memory()
        model = SelectField(choices=models)
        mem = SelectField(coerce=int,choices=memory)

    form = SelectTeamForm()

    if form.is_submitted():
        print("Submitted")

    if form.validate():
        print("Valid")

    print(form.errors)

    # handle post request in form
    if form.validate_on_submit():
        session['MODEL'] = form.model.data
        print("WAS HERE")
        session['MEMORY'] = form.mem.data
        return redirect('/itemResults')

    return render_template("itemSearch.html", form=form)

# Page that we got to after a itemSearch is submit and valid
@app.route('/itemResults', methods=['GET','POST'])
def results():

    model = session['MODEL']
    memory = session['MEMORY']
    items = db.get_phones(model,memory)
    items = db.pandafy(items,"TITLE")

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

# Page that lets us search transactions by email
@app.route('/TransactionSearch', methods=['GET','POST'])
def TransactionSearch():
    class SelectEmailForm(FlaskForm):
         emails = db.get_emails()
         email = SelectField(choices=emails)

    form2 = SelectEmailForm()

    if form2.is_submitted():
        print("Submitted")

    if form2.validate():
        print("Valid")

    print(form2.errors)

    # handle post request in form
    if form2.validate_on_submit():
        session['EMAIL'] = form2.email.data
        return redirect('/transactionResults')

    return render_template("TransactionSearch.html", form2=form2)

# Page that displays the results of the previous page
@app.route('/transactionResults', methods=['GET','POST'])
def transactionResults():

    email = session['EMAIL']
    emails = db.users_trans(email)
    emails = db.pandafy(emails,"NAME")

    return render_template("transactionResults.html", tables=[emails.to_html()])

# Displays the best buys and returns
@app.route('/bestBuys', methods=['POST','GET'])
def bestBuys():
    gains = db.biggest_gains()
    gains = db.pandafy(gains,"CUST_ID")

    returns = db.weakly_returns()
    returns = db.pandafy(returns,"ITEM_ID")


    return render_template("bestBuys.html", tables= [gains.to_html(),returns.to_html()])



'''
# create simple api that takes in id and response with stats of said player
# ex http://localhost:5000/api/201960
# TODO add query parameters like http://localhost:5000/api?id=201960
@app.route('/api/<id>', methods=['GET','POST'])
def api(id):
    player_id = id
    stats = db.get_stats(player_id)
    return jsonify(stats)
'''

if __name__ == '__main__':
    app.run(debug=True, host='localhost')
