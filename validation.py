import os
from json import loads as json_loads

from googleapiclient import discovery
from googleapiclient.errors import HttpError


VALIDATION_LIMITS = {
    "TOXICITY": 0.70,
    "INSULT": 0.50,
    "IDENTITY_ATTACK": 0.30,
    "SEXUALLY_EXPLICIT": 0.20,
    "THREAT": 0.20,
    "PROFANITY": 0.40
}


"""
External API Validation
"""
def analyze_text_with_perspective(text: str):
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.environ.get("PERSPECTIVE_API_KEY"),
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": f"{text}"},
        "requestedAttributes": {"TOXICITY": {}, "IDENTITY_ATTACK": {}, "THREAT": {}, "SEXUALLY_EXPLICIT": {}, "INSULT": {}, "PROFANITY": {}}
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
    except HttpError as e:
        err = json_loads(e.content)["error"]

        return False, err["status"]

    return True, response["attributeScores"]

def validate_title(title: str):
    succ, validation_res = analyze_text_with_perspective(title)
    if not succ:
        if "INVALID_ARGUMENT" in validation_res:
            return False, "Invalid title"

        return False, validation_res.replace("_", " ").title()

    for category, limit in VALIDATION_LIMITS.items():
        score = validation_res[category]["spanScores"][0]["score"]["value"]

        if score > limit:
            return False, category.replace("_", " ").title()

    return True, ""


