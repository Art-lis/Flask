import os

from flask import Flask
from random import randint

app = Flask(__name__)

version = '1.9'
archivePath = '/archive'
outputFile = 'output.txt'

@app.route('/get-item',endpoint='get-item' ,methods=['GET'])
def main():
    envVar = os.environ.get('NUMBER_TYPE')
    choice = False

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


    randstr = str(randnum)
    if not os.path.exists(archivePath):
        print('no volume attached')
    else:
        f = open(archivePath+'/'+outputFile, 'a')
        f.write(randstr+'\n')
        f.close()

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