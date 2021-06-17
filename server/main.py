import json

from dateutil import parser
from flask import Flask
from flask import request
from flask_prometheus_metrics import register_metrics
from prometheus_client import make_wsgi_app, Gauge, CollectorRegistry, push_to_gateway
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app = Flask(__name__)

DATA_FILE = "elektrina_data.txt"


registry = CollectorRegistry()

test_endpoint = Gauge('test_metric', 'testovaci endpoint', registry=registry)
data_endpoint = Gauge('data_metric', 'ledkovaci endpoint', registry=registry)



@app.route("/")
def index():
    test_endpoint.inc(20)
    push_to_gateway()
    return "Test"


@app.route('/new-data', methods=['POST'])
def new_data():
    date = json.loads(request.data)["data"]
    parsedDate = parser.parse(date)
    print(parsedDate)
    try:
        with open(DATA_FILE, "a") as data_file:
            data_file.write(f"{date}\n")
    except Exception as e:
        return f"error - {e}"
    return 'ok'


register_metrics(app, app_version="v0.1.2", app_config="staging")
dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

if __name__ == "__main__":
    run_simple(hostname="0.0.0.0", port=5050, application=dispatcher)
