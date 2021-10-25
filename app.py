from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("index.html", title="Welcome")

@app.route("/test1")
def test1():
    return render_template("test1.html", title="Testing")

@app.route("/login", methods=["POST"])
def login():
    1+1

if __name__ == "__main__":
    app.run(port=5000, debug=True)