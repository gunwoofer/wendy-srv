from flask import Flask
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)

@app.route('/createWeekend', methods=['POST'])
def create_weekend():
    print('Request received !!')
    return jsonify(
        greeting="Hello from Flask !"
    )

if __name__ == '__main__':
    app.run(port=3000)