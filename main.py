import os

from flask import Flask
from random import randint

app = Flask(__name__)

version = '1.4'
archivePath = '/Flask/archive'
outputFile = 'output.txt'

@app.route('/get-item',endpoint='get-item' ,methods=['GET'])
def main():
    randnum = str(randint(0, 1000))
    if not os.path.exists(archivePath):
        os.mkdir(archivePath)
    f = open(archivePath+'/'+outputFile, 'a')
    f.write(randnum+'\n')
    f.close()
    return randnum


@app.route('/author', endpoint='author', methods=['GET'])
def author():
    return 'Artur Liszewski'

if __name__ == '__main__':
    print('### Version: '+version+' ###')
    app.run(debug=True, host='0.0.0.0')