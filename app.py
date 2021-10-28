from flask import Flask, render_template, request, flash, session
import datetime
import requests
from werkzeug.utils import redirect
import data_from_veikkaus as dfv
app = Flask(__name__)
defdate1 = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(weeks=1),'%Y-%m-%d')
defdate2 = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')

@app.route("/")
def welcome():
    return render_template("index.html", title="Welcome")

@app.route("/test1")
def test1():
    return render_template("test1.html", title="Testing1")

@app.route("/test2")
def test2():
    return render_template("test2.html", title="Testing2", defdate1 = defdate1, defdate2=defdate2)

@app.route("/getdata", methods=["POST"])
def getdata():
    startdate = datetime.datetime.strptime(request.form['startdate'],'%Y-%m-%d')
    enddate = datetime.datetime.strptime(request.form['enddate'],'%Y-%m-%d')
    if startdate > enddate:
        startdate,enddate = enddate,startdate
    print(startdate)
    print(enddate)
    dfv.handle_data(startdate,enddate)
    return render_template("test2.html", title="Testing2", defdate1 = startdate.strftime('%Y-%m-%d'),defdate2 = enddate.strftime('%Y-%m-%d'))

@app.route("/form")
def form():
    return render_template("login.html", title="Login")

@app.route("/data")
def data():
    return render_template("data.html", title="Data")

@app.route("/login", methods=["POST"])
def login():
    if request.form["username"]=="admin" and request.form["password"]=="admin":
        return render_template('loggedin.html', title="Successful login")
    else:
        return render_template('login.html', title="Failed login")

if __name__ == "__main__":
    app.run(port=5000, debug=True)