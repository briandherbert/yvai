# To get this app working:
# python3 -m venv venv
# source venv/bin/activate
# pip3 install .
# export FLASK_APP=yvai.py
# export OPENAI_API_KEY=
# export PASSARG=
# export SHEETID=
# flask run --reload

# if dependencies aren't found, the app may not be running from venv, can verify from the print(sys.path)

from flask import Flask, request, Response, jsonify
from API_openai import getChatGPTAnswer
import DB_gsheets
import sys
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

PASSARG = "none"

def verify(request):
    print('Verifying request', file=sys.stderr)
    global PASSARG

    try:
        if PASSARG == "none":
            PASSARG = os.getenv("PASSARG")

        passarg = request.get_json(force=True)["PASSARG"]
        print(f'Passargs {passarg} {PASSARG}')

        return passarg == PASSARG
    except:
        return False

@app.route('/ask', methods = ['POST', 'GET'])
def ask():
    if not verify(request): return "!"

    json = request.get_json(force=True)
    prompt = json["prompt"]

    promptAdd = DB_gsheets.getPromptAdd()
    if promptAdd:
        prompt = promptAdd + prompt

    print(f"got prompt {prompt}")

    systemPrompt = DB_gsheets.getSystemPrompt()

    maxTokens = DB_gsheets.getMaxTokens()
    response = getChatGPTAnswer(prompt, max_tokens=maxTokens, system_prompt=systemPrompt)

    return {"response": response}, 200

@app.route('/prompteng', methods = ['POST', 'GET'])
def getPromptEng():
    if not verify(request): return "!"

    print(f'hitting prompt eng endpoint', file=sys.stderr)
    return DB_gsheets.getPromptAdd()

@app.route('/topic', methods = ['POST', 'GET'])
def topic():
    if not verify(request): return "!"

    answer = "Error"

    try:
        topics = DB_gsheets.getTopics()
        prompt = f"Using one of these topics as your only response {topics} , classify the following : "
        prompt += request.get_json(force=True)["prompt"]
        answer = getChatGPTAnswer(prompt)
    except:
        pass
    return {"response": answer}, 200

@app.route('/debug', methods = ['POST', 'GET'])
def debug():
    print("hit debug")
    info = ""

    try:
        info += "Url params " + str(request.args) + "<br>\n"
    except:
        print("no params")
        pass

    try:
        info += "JSON: " + str(request.get_json(force=True)) + "<br>\n"
    except:
        print("no json")
        pass

    try:
        info += "Data: " + str(request.get_data()) + "<br>\n"
    except:
        print("no data")
        pass

    print("info " + info)
    return {"response": info}, 200


@app.route('/', methods = ['POST', 'GET'])
@app.route('/index', methods = ['POST', 'GET'])
def index():
    return {"response": "default"}, 200

