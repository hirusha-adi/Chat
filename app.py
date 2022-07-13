# libraries
from flask import Flask, render_template, request
from prsaw import RandomStuffV2

# chat initialization

app = Flask(__name__)
rs = RandomStuffV2()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    response = rs.get_ai_response(msg)
    res = (response['message'])
    print(response)
    print(res)
    return "hey"


if __name__ == "__main__":
    app.run()
