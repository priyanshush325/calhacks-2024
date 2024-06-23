import json
import os
import argparse
import glob

from dotenv import load_dotenv
from openai import OpenAI
from util.files import *
from util.prompting import *
from util.coding import *
from util.coding import ProjectInfo
from util.ui import *

import subprocess
import threading
import queue
import sys
import time

load_dotenv()

parser = argparse.ArgumentParser()

parser.add_argument("directory")
parser.add_argument("port")


args = parser.parse_args()

# print(args.directory)

client = OpenAI()
MODEL = "gpt-4o"
# PROJECT_DIRECTORY = "./frontend/src"
PROJECT_SOURCE_DIRECTORY = args.directory + "/src"

# Search through Project source directory for .priyanshu file
search_pattern = os.path.join(args.directory, "*.priyanshu")

files = glob.glob(search_pattern)

if len(files) != 1:
    print("Make sure there is exactly 1 .priyanshu file in the source directory")
    exit(1)

print(f"Found .priyanshu file: {files[0]}")
print(f"Project source directory: {PROJECT_SOURCE_DIRECTORY}")
print(f"Running project on {args.port}")
# print a localhost link
print(f"Localhost: http://localhost:{args.port}")
print("---------------------------------------")
INFO_PATH = files[0]


# INFO_PATH = PROJECT_SOURCE_DIRECTORY + "/repoinfo.priyanshu"

PROJECT_INFO = ProjectInfo(
    "Calculator App", PROJECT_SOURCE_DIRECTORY, INFO_PATH)

UI_PORT = args.port
PROJECT_PORT = int(args.port) + 1

##########################
# Start the project server
##########################

WEBSERVER_OUTPUT = "./generator-logs/webserver.txt"
WEBSERVER_OUTPUT_ABSOLUTE = os.path.abspath(WEBSERVER_OUTPUT)
if not os.path.exists("./generator-logs"):
    os.mkdir("./generator-logs")
if not os.path.exists(WEBSERVER_OUTPUT):
    with open(WEBSERVER_OUTPUT, 'w') as f:
        f.write("")
originalDirectory = os.getcwd()
os.chdir(args.directory)
command = f"npm run dev -- --port {UI_PORT}"
command += f" 2>{WEBSERVER_OUTPUT_ABSOLUTE}"
command += f" 1>{WEBSERVER_OUTPUT_ABSOLUTE}"
command += f" < /dev/null &"
process = subprocess.Popen(
    command,
    shell=True,
    text=True
)
os.chdir(originalDirectory)

##########################

# Start the UI
startUI(UI_PORT, PROJECT_PORT)

while True:
    newPrompt = input("Add prompt: ")
    # handleFeaturePrompt(newPrompt)

    if newPrompt.startswith("xx"):
        print("You're welcome!")
        break
    elif newPrompt.startswith("!fix"):
        print("Fixing the error")

        error_lines = get_latest_error_lines(WEBSERVER_OUTPUT_ABSOLUTE)

        if len(error_lines) == 0:
            print("No error found")
            continue

        pr = "Fix the following error. Keep in mind that the root cause of the error may not be what is shown in the error message.\n"
        if len(newPrompt) > 10:
            pr += newPrompt[5:]

        pr += "\n".join(error_lines)

        createActionPlan(pr, client, MODEL, PROJECT_INFO)

    elif len(newPrompt) < 10:
        pass
    else:
        createActionPlan(newPrompt, client, MODEL, PROJECT_INFO)
