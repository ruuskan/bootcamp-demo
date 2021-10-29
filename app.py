from flask import Flask, render_template, request, flash, session
import datetime
import requests
from werkzeug.utils import redirect
import data_from_veikkaus as dfv
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY']='keepitsecretkeepitsafe'
load_dotenv()

@app.route("/")
def welcome():
    return render_template("index.html", title="Welcome")

@app.route("/test1")
def test1():
    return render_template("test1.html", title="Testing1")

@app.route("/test2")
def test2():
    defdate1 = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(weeks=1),'%Y-%m-%d')
    defdate2 = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
    return render_template("test2.html", title="Testing2", defdate1 = defdate1, defdate2=defdate2)

@app.route("/getdata", methods=["POST"])
def getdata():
    if ('loggedin' in session) & ('sync' in request.form):
        startdate = datetime.datetime.strptime(request.form['startdate'],'%Y-%m-%d')
        enddate = datetime.datetime.strptime(request.form['enddate'],'%Y-%m-%d')
        if startdate > enddate:
            startdate,enddate = enddate,startdate
        dfv.handle_data(startdate,enddate)
        return render_template("test2.html", title="Testing2", defdate1 = startdate.strftime('%Y-%m-%d'),defdate2 = enddate.strftime('%Y-%m-%d'))
    return redirect("/data")
@app.route("/login")
def login():
    return render_template("login.html", title="Login")

@app.route("/data")
def data():
    return render_template("data.html", title="Data")

@app.route("/loginsubmit", methods=["POST", 'GET'])
def loginsubmit():
    if request.method=='GET':
        redirect('/login')
    else:
        if request.form['username']==os.environ['APP_USER'] and request.form["password"]==os.environ['APP_PASSWORD']:
            session['loggedin'] = True
            return render_template('logout.html', title="Successful login")
        else:
            return redirect('login')

@app.route("/logout")
def logout():
    return render_template("logout.html", title="Log out")

@app.route("/logoutsubmit", methods=["POST"])
def logoutsubmit():
    session.pop('loggedin',None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(port=5000, debug=True)