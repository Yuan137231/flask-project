from flask import Flask
app = Flask(__name__)
print(__name__)
print(app)

@app.route("/")
def hello():
    return "<h1>Hello World!<h1>"

@app.route("/user/<name>")
def user(name):
    return f"<h1>Hello {name}!<h1>"

if __name__ == '__main__':
    app.run(debug=True)