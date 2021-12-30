import datetime
import os
import time

import requests
from flask import Flask, g
from random import randint
from google.cloud import storage
from google.cloud import bigquery

app = Flask(__name__)

version = '2.8'
archivePath = '/archive'
outputFile = 'output.txt'

@app.before_request
def before_request():
   g.request_start_time = time.time()
   g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

@app.route('/', methods=['GET'])
def start():
    return 'aplikacja flaska tylko że rapowa'


@app.route('/get-item', endpoint='get-item', methods=['GET'])
def main():
    envVar = os.environ.get('NUMBER_TYPE')
    choice = False

    # sprawdzenie czy parzysta / nieparzysta / dowolna
    while choice == False:
        randnum = randint(0, 1000)
        if envVar == 'even':
            if isEven(randnum):
                choice = True
        elif choice == 'odd':
            if isOdd(randnum):
                choice = True
        else:
            choice = True

    # zapis na pod
    randstr = str(randnum)
    if not os.path.exists(archivePath):
        print('no volume attached')
    else:
        f = open(archivePath + '/' + outputFile, 'a')
        f.write(randstr + '\n')
        f.close()

    # upload do bucketa
    date = str(datetime.datetime.now()).replace(' ', '_')
    bucketName = os.environ.get('BUCKET_NAME')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucketName)
    blob = bucket.blob(date)
    blob.upload_from_string(randstr)

    # upload do BigQuery
    #client = bigquery.Client.from_service_account_json('serv-acc.json', project='artur-liszewski')
    client = bigquery.Client()
    table_id = 'python_flask.python_flask_table'


    rows_to_insert = [
        {u"execution_time": str(g.request_time()), u"number": randstr, u"timestamp": date, u"deployment": os.environ.get('DEPLOYMENT')},
    ]

    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")

    return randstr


def isEven(num):
    if num % 2 == 0:
        return True
    else:
        return False


def isOdd(num):
    if num % 2 != 0:
        return True
    else:
        return False


@app.route('/author', endpoint='author', methods=['GET'])
def author():
    author = 'Artur Liszewski<br>'
    podName = os.environ.get('MY_POD_NAME') or ''
    nodeName = os.environ.get('MY_NODE_NAME') or ''
    bucketName = os.environ.get('BUCKET_NAME')
    output = str(author) + '<br>' + str(nodeName) + '<br>' + str(podName) + '<br>' + bucketName
    return output

@app.route('/prime', methods=['GET'])
def prime():
    liczba = requests.get('https://us-central1-artur-liszewski.cloudfunctions.net/function-1').text
    return str(liczba)

@app.route('/error', methods=['GET'])
def error():
    return 1


if __name__ == '__main__':
    print('### Version: ' + version + ' ###')
    app.run(debug=True, host='0.0.0.0')
