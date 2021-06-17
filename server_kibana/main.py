import json
from datetime import datetime

from dateutil import parser
from elasticsearch import Elasticsearch
from flask import Flask
from flask import request

app = Flask(__name__)

DATA_FILE = "elektrina_data.txt"

es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

res = es.index(index="test-index", body=doc)
print(res['result'])


es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

@app.route("/")
def index():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
