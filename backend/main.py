import requests
from firebase import firebase
from flask import Flask, jsonify, request
from flask_cors import CORS


firebase = firebase.FirebaseApplication(
    'https://calhacks-2024-default-rtdb.firebaseio.com/', None)

app = Flask(__name__)

CORS(app)


@app.route('/people', methods=['GET'])
def get_people():
    people = firebase.get('/people', None)
    return jsonify(people)


if __name__ == "__main__":
    app.run(debug=True)
