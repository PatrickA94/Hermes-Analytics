from flask import Flask, render_template, redirect, jsonify, url_for, request, session
from flask_restful import Api
import simplejson
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


@app.route('/', methods=['GET', 'POST'])
def index():
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
        return redirect('/player')

    return render_template("index.html", form=form)


@app.route('/player', methods=['GET','POST'])
def player():

    model = session['MODEL']
    memory = session['MEMORY']
    items = db.get_phones(model,memory)
    items = simplejson.dumps(items)
    items = pd.read_json(items)
    items.set_index(['TITLE'],inplace=True)
    items['URL'] =items["URL"].apply('<a href="{0}">{0}</a>'.format)


    #items["URL"] = items["URL"]
    items.index.name=None

    return render_template("player.html", tables=[items.to_html()])


@app.route('/stats', methods=['POST', 'GET'])
def stats():
    player_id = session['PLAYER_ID']
    stats = db.get_stats(player_id)

    return render_template("stats.html", name=stats[1], blocks=stats[9], drfgm=stats[11], drfga=stats[12], drfgpct=stats[13])

# create simple api that takes in id and response with stats of said player
# ex http://localhost:5000/api/201960
# TODO add query parameters like http://localhost:5000/api?id=201960
@app.route('/api/<id>', methods=['GET','POST'])
def api(id):
    player_id = id
    stats = db.get_stats(player_id)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, host='localhost')

