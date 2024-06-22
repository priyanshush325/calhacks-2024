import requests
from firebase import firebase
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json



app = Flask(__name__)
CORS(app)
firebase = firebase.FirebaseApplication('https://calhacks-2024-default-rtdb.firebaseio.com/', None)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#Utility Functions
def getPeople(): 
    people = firebase.get('/people', None)
    return people


@app.route('/people', methods=['GET'])
def get_people():
    return getPeople()

@app.route('/people/risk', methods=['GET'])
def get_risk():
    people = getPeople()
    person = people[2]
    print(person)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_API_KEY
    }

    data = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a medical risk calculator. Your job is to find out if you have a high risk of developing a disease. For each disease that a user is at risk for, you should return one of the following: 'High', 'Moderate', or 'Low', along with a percentage approximation of the chances of developing the disease. Return ONLY a JSON object where the keys are the names of the disease, and the values are an array where the first item is the risk level and the second item is the risk percentage."
            },
            {
                "role": "user",
                "content": f"Is {person} at risk for any diseases?"
            }
        ],
        "temperature": 0.4
    })

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=data)
    response_json = response.json()
    print(response_json)
    risk_content = response_json['choices'][0]['message']['content']
    
    # Parse the string as a JSON object
    risk_content_dict = json.loads(risk_content)
    
    return jsonify(risk_content_dict)

if __name__ == "__main__":
    app.run(debug = True)

