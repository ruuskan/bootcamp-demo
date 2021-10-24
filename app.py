from flask import Flask

app = Flask(__name__)

@app.route("/")
def test():
    return "Hello world!"

if __name__ == "__main__":
    app.run(port=5000)