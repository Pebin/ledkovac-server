import json
import logging
import os

from dateutil import parser
from elasticsearch import Elasticsearch
from flask import Flask
from flask import request

app = Flask(__name__)

DATA_FILE = "elektrina_data.txt"

elastic_url = os.getenv("ELASTICSEARCH_URL", "localhost")
es = Elasticsearch([elastic_url])

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ledkovac-server')


def get_hits_in_elastic():
    return es.search(index="flash-data", body={"query": {"match_all": {}}})


@app.route("/")
def index():
    return "Test"


@app.route("/data-count")
def data_count():
    try:
        hits = get_hits_in_elastic()['hits']['total']['value']
        return f"hits in elastic - {hits}", 200
    except Exception as ex:
        logger.info(f"Could not read flash-data from elastic: {ex}"), 400


@app.route('/new-data', methods=['POST'])
def new_data():
    data_id = json.loads(request.data)["id"]
    date = json.loads(request.data)["date"]
    parsed_date = parser.parse(date)
    try:
        with open(DATA_FILE, "a") as data_file:
            data_file.write(f"{date}\n")
        result = es.index(index="flash-data", body={'id': data_id, 'timestamp': parsed_date})
        logger.info(f"{data_id} - {date} : {result['result']}")
    except Exception as ex:
        return f"error - {ex}", 400
    return 'ok', 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5600)
