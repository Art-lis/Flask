import os

from flask import Flask
from random import randint

app = Flask(__name__)

version = '1.8'
archivePath = '/archive'
outputFile = 'output.txt'

@app.route('/get-item',endpoint='get-item' ,methods=['GET'])
def main():
    randnum = str(randint(0, 1000))
    if not os.path.exists(archivePath):
        print('no volume attached')
    else:
        f = open(archivePath+'/'+outputFile, 'a')
        f.write(randnum+'\n')
        f.close()
    return randnum


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