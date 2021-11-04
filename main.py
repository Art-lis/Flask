from flask import Flask
from random import randint

app = Flask(__name__)

@app.route('/get-item',endpoint='get-item' ,methods=['GET'])
def main():
    return str(randint(0, 1000))


@app.route('/author', endpoint='author', methods=['GET'])
def author():
    return 'Artur Liszewski'

if __name__ == '__main__':
    app.run(debug=True)