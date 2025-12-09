from flask import Flask, request, session, current_app, jsonify
from flask import render_template;
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from json import loads as json_loads
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


@app.route('/')
def index_page():

    return render_template("index.html")

@app.route('/validate', methods=['POST'])
def validate():
    body = request.get_json()
    comment = body['comment']

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.environ.get("PERSPECTIVE_API_KEY"),
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    )

    analyze_request = {
        "comment": {"text": comment},
        "requestedAttributes": {
            "TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "INSULT": {},
            "PROFANITY": {}
        }
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        print(response)
    except HttpError as e:
        err = json_loads(e.content)["error"]
        return jsonify({"success": False, "error": err["status"]}), 400

    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)