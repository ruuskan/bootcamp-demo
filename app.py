from flask import Flask, render_template, request, flash, session
import datetime
import requests
from werkzeug.utils import redirect
import data_from_veikkaus as dfv
import os
from dotenv import load_dotenv
from analysis import data_analysis

app = Flask(__name__)
app.config['SECRET_KEY']='keepitsecretkeepitsafe'
load_dotenv()

data = {}

@app.route("/")
def welcome():
    global data
    if 'dt_start' not in data:
        data['dt_start'] = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(weeks=1),'%Y-%m-%d')
    if 'dt_end' not in data:
        data['dt_end'] = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
    
    title = 'Data analysed' if 'analysis' in session else 'Welcome'
    return render_template("index.html", title=title, data = data)


@app.route("/getdata", methods=["POST"])
def getdata():
    global data
    startdate = datetime.datetime.strptime(request.form['startdate'],'%Y-%m-%d')
    enddate = datetime.datetime.strptime(request.form['enddate'],'%Y-%m-%d')
    if startdate > enddate:
        startdate,enddate = enddate,startdate
    data['dt_start'] = datetime.datetime.strftime(startdate,'%Y-%m-%d')
    data['dt_end'] = datetime.datetime.strftime(enddate,'%Y-%m-%d')
    if ('loggedin' in session) & ('sync' in request.form):
        dfv.handle_data(startdate,enddate)
    elif ('download' in request.form):
        #TODO
        pass
    return redirect("/data")

@app.route("/login")
def login():
    return render_template("login.html", title="Login")

@app.route("/data")
def datafunc():
    global data
    if 'dt_start' not in data:
        data['dt_start'] = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(weeks=1),'%Y-%m-%d')
    if 'dt_end' not in data:
        data['dt_end'] = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
    return render_template("data.html", title="Data", data=data)

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

@app.route("/analyse", methods=["POST"])
def analyse():
    if 'clear' in request.form:
        session.pop('analysis',None)
    else:
        global data
        startdate = datetime.datetime.strptime(request.form['startdate'],'%Y-%m-%d')
        enddate = datetime.datetime.strptime(request.form['enddate'],'%Y-%m-%d')
        if startdate > enddate:
            startdate,enddate = enddate,startdate
        data['dt_start'] = datetime.datetime.strftime(startdate,'%Y-%m-%d')
        data['dt_end'] = datetime.datetime.strftime(enddate,'%Y-%m-%d')
        data_analysed = data_analysis(startdate, enddate)
        if data_analysed != {}:
            session['analysis'] = True 
            for key in data_analysed.keys():
                data[key] = data_analysed[key]
    return redirect("/")


if __name__ == "__main__":
    app.run(port=5000, debug=True)