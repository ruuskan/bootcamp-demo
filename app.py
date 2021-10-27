from flask import Flask, render_template, request, flash, session

app = Flask(__name__)


logged = False
print(logged)
@app.route("/")
def welcome():
    return render_template("index.html", title="Welcome", loggedin=logged)

@app.route("/test1")
def test1():
    return render_template("test1.html", title="Testing", loggedin=logged)

@app.route("/form")
def form():
    return render_template("login.html", title="Login", loggedin=logged)

@app.route("/data")
def data():
    return render_template("data.html", title="Data", loggedin=logged)

@app.route("/login", methods=["POST"])
def login():
    if request.form["username"]=="admin" and request.form["password"]=="admin":
        logged = True
        return render_template('loggedin.html', title="Successful login", loggedin=logged)
    else:
        logged = False
        return render_template('login.html', title="Failed login", loggedin=logged)

if __name__ == "__main__":
    app.run(port=5000, debug=True)