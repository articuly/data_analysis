# -*- coding=utf-8 -*-
from flask import Flask, render_template, make_response, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api")
def api():
    response = make_response("ok")
    # response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/test_jsonp")
def test():
    import json
    callback = request.args.get("callback")
    message = {"status": "success", "data": " it's fine"}
    response = callback + "(" + json.dumps(message) + ")"
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5002", debug=True, load_dotenv=True)
