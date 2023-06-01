import requests
import csv
from io import StringIO
import sys
import os

# first int is row, next is col
PROMPT_CELL = [1,0]
SYSTEM_PROMPT_CELL = [1,1]
TOPICS_COL = 2
TOKENS_CELL = [1,3]

DATA_CACHE = None

DEFAULT_BUST_CACHE = True

SHEET_ID = os.getenv("SHEETID")

def getCSVData(bustCache = DEFAULT_BUST_CACHE):
    global DATA_CACHE

    if bustCache or not DATA_CACHE:    
        url = f"https://docs.google.com/spreadsheets/d/e/{SHEET_ID}/pub?output=csv"

        response = requests.get(url)
        assert response.status_code == 200, 'Wrong status code'

        reader = csv.reader(StringIO(response.text))
        DATA_CACHE = list(reader)
    return DATA_CACHE

def getPromptAdd(bustCache = DEFAULT_BUST_CACHE):
    data = getCSVData(bustCache)
    return data[PROMPT_CELL[0]][PROMPT_CELL[1]]

def getSystemPrompt(bustCache = DEFAULT_BUST_CACHE):
    data = getCSVData(bustCache)
    return data[SYSTEM_PROMPT_CELL[0]][SYSTEM_PROMPT_CELL[1]]

def getMaxTokens(bustCache = DEFAULT_BUST_CACHE):
    data = getCSVData(bustCache)
    return data[TOKENS_CELL[0]][TOKENS_CELL[1]]

def getTopics(bustCache = DEFAULT_BUST_CACHE):
    topics = []
    data = getCSVData(bustCache)

    i = 1
    while (True):
        if i >= len(data):
            break

        topic = data[i][TOPICS_COL]
        if not topic:
            break
        topics.append(topic)
        i += 1
    return topics

#print(getPromptAdd())
# print(getTopics())