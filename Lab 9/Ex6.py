import json

filename = "quiz_data.json"

with open(filename, "r") as jsonfile:
    questions = json.load(jsonfile)

print(json.dumps(questions, indent=4))