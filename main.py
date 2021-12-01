import datetime
import os

from flask import Flask
from random import randint
from google.cloud import storage

app = Flask(__name__)

version = '2.2'
archivePath = '/archive'
outputFile = 'output.txt'

@app.route('/get-item',endpoint='get-item' ,methods=['GET'])
def main():
    envVar = os.environ.get('NUMBER_TYPE')
    choice = False

    #sprawdzenie czy parzysta / nieparzysta / dowolna
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

    #zapis na pod
    randstr = str(randnum)
    if not os.path.exists(archivePath):
        print('no volume attached')
    else:
        f = open(archivePath+'/'+outputFile, 'a')
        f.write(randstr+'\n')
        f.close()

    #upload do bucketa
    date = str(datetime.datetime.now()).replace(' ', '_')
    bucketName = os.environ.get('BUCKET_NAME')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucketName)
    blob = bucket.blob(date)
    blob.upload_from_string(randstr)

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
    podName = os.environ.get('MY_POD_NAME')
    nodeName = os.environ.get('MY_NODE_NAME')
    bucketName = os.environ.get('BUCKET_NAME')
    output = str(author)+'<br>'+str(nodeName)+'<br>'+str(podName)+'<br>'+bucketName
    return output

if __name__ == '__main__':
    print('### Version: '+version+' ###')
    app.run(debug=True, host='0.0.0.0')