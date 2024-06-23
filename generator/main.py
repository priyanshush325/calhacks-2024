from flask import Flask, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
from util.coding import ProjectInfo
from openai import OpenAI
from util.files import *
from util.prompting import *
from util.coding import *
from util.coding import ProjectInfo

import subprocess
import threading
import glob
import queue
import sys
import time
import socket
import os

app = Flask(__name__)
CORS(app)
load_dotenv()

client = OpenAI()
MODEL = "gpt-4o"

UI_PORT = 5173
PROJECT_PORT = 5174

# Declare global variables at the module level
ROOT_DIRECTORY = None
PROJECT_SOURCE_DIRECTORY = None
INFO_PATH = None
PROJECT_INFO = None
WEBSERVER_OUTPUT_ABSOLUTE = None
PENDING_ACTIONS = None

# Utility Functions
def processPrompt(prompt):
    global PROJECT_INFO
    global PROJECT_SOURCE_DIRECTORY
    global PENDING_ACTIONS

    print(PROJECT_INFO)
    print(PROJECT_SOURCE_DIRECTORY)
    
    newPrompt = prompt
    # handleFeaturePrompt(newPrompt)

    if newPrompt.startswith("xx"):
        print("You're welcome!")
        return
    elif newPrompt.startswith("!fix"):
        print("Fixing the error")
        global WEBSERVER_OUTPUT_ABSOLUTE
        WEBSERVER_OUTPUT_ABSOLUTE = os.path.abspath("generator/webserver/output.log")
        error_lines = get_latest_error_lines(WEBSERVER_OUTPUT_ABSOLUTE)

        if len(error_lines) == 0:
            print("No error found")
            return

        pr = "Fix the following error. Keep in mind that the root cause of the error may not be what is shown in the error message.\n"
        if len(newPrompt) > 10:
            pr += newPrompt[5:]

        pr += "\n".join(error_lines)

        PENDING_ACTIONS = APIActionPlan(pr, client, MODEL, PROJECT_INFO)
        return PENDING_ACTIONS, 200

    elif len(newPrompt) < 10:
        pass
    else:
        PENDING_ACTIONS = APIActionPlan(newPrompt, client, MODEL, PROJECT_INFO)
        return PENDING_ACTIONS, 200

def confirmActions():
    global PENDING_ACTIONS
    print("PENDING_ACTIONS: ", PENDING_ACTIONS)
    if PENDING_ACTIONS is None:
        return "No actions found", 400
    else:

        # run the commands
        for command in PENDING_ACTIONS["commands"]:
            runCommandInDirectory(command, PROJECT_INFO.projectSourceDir)

        # Execute actions

        allContextFiles = {}
        for action in PENDING_ACTIONS["actions"]:
            for file in action.contextFiles:
                if checkFileExists(file):
                    allContextFiles[file] = readFile(file, False)
        for action in PENDING_ACTIONS["actions"]:
            print(f"Action: {action.action}, File: {action.filePath}, Prompt: {action.prompt}")
            executeAction(action, client, MODEL, PROJECT_INFO, allContextFiles)
        return "Actions executed", 200

@app.route("/prompt", methods=["POST"])
def prompt():
    processPrompt(request.json["prompt"])
    return "success", 200

@app.route("/info", methods=["POST"])
def info():
    global ROOT_DIRECTORY
    global PROJECT_SOURCE_DIRECTORY
    global INFO_PATH
    global PROJECT_INFO

    ROOT_DIRECTORY = request.json["projectSourceDir"]
    PROJECT_SOURCE_DIRECTORY = os.path.join(ROOT_DIRECTORY, "src")

    # Search through Project source directory for .priyanshu file
    search_pattern = os.path.join(ROOT_DIRECTORY, "*.priyanshu")
    files = glob.glob(search_pattern)

    if len(files) != 1:
        print("Make sure there is exactly 1 .priyanshu file in the source directory")
        return "failure", 400
    
    print(f"Found .priyanshu file: {files[0]}")
    INFO_PATH = files[0]

    PROJECT_INFO = ProjectInfo(
        "Calculator App", PROJECT_SOURCE_DIRECTORY, INFO_PATH)
    
    print(f"Project Info: {PROJECT_INFO}")
    print(f"Project Source Directory: {PROJECT_SOURCE_DIRECTORY}")
    print(f"Project Info Path: {INFO_PATH}")
    return "success", 200

@app.route("/confirm", methods=["POST"])
def confirm():
    confirmActions()
    return "success", 200

if __name__ == "__main__":
    app.run(debug=True)
