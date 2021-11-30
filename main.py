import datetime
import os

from flask import Flask
from random import randint
from google.cloud import storage

app = Flask(__name__)

version = '2.6'
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
    #upload_blob(bucketName, randstr, date)
    storage_client = storage.Client.from_service_account_json(
        'service-account-file.json')
    bucket = storage_client.bucket(bucketName)
    blob = bucket.blob(date+'.txt')
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
    output = str(author)+'<br>'+str(nodeName)+'<br>'+str(podName)
    return output

if __name__ == '__main__':
    print('### Version: '+version+' ###')
    app.run(debug=True, host='0.0.0.0')


#def upload_blob(bucket_name, data, destination_blob_name):
#    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

#    storage_client = storage.Client.from_service_account_json(
#        'service-account-file.json')
#    bucket = storage_client.bucket(bucket_name)
#    blob = bucket.blob(destination_blob_name)

#    blob.upload_from_string(data)

#    print(
#        "File {} uploaded to {}.".format(
#            data, destination_blob_name
#        )
#    )