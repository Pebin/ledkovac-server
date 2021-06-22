import json

from dateutil import parser
from elasticsearch import Elasticsearch
from flask import Flask
from flask import request

app = Flask(__name__)

DATA_FILE = "elektrina_data.txt"

es = Elasticsearch()

try:
    res = es.search(index="flash-data", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
except Exception as ex:
    print(f"Could not read flash-data from elastic: {ex}")


@app.route("/")
def index():
    return "Test"


@app.route('/new-data', methods=['POST'])
def new_data():
    data_id = json.loads(request.data)["id"]
    date = json.loads(request.data)["date"]
    parsed_date = parser.parse(date)
    try:
        with open(DATA_FILE, "a") as data_file:
            data_file.write(f"{date}\n")
            result = es.index(index="flash-data", body={'id': data_id, 'timestamp': parsed_date})
            print(f"{data_id} - {date} : {result['result']}")
    except Exception as ex:
        return f"error - {ex}"
    return 'ok'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
