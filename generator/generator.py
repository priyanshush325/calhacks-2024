import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from util.files import *
from util.prompting import *

load_dotenv()

client = OpenAI()
MODEL = "gpt-4o"


# looks in ../frontend/src and returns a tree of all the files
def fetchProjectTree():
    projectTree = []
    directory = "./frontend/src"

    try:
        for root, dirs, files in os.walk(directory):
            print(f"Visiting {root}, Directories: {
                  dirs}, Files: {files}")  # Debugging output
            for file in files:
                projectTree.append(os.path.join(root, file))
    except Exception as e:
        print(f"An error occurred: {e}")  # Error handling output
    return projectTree


def readFile(file):
    content = ""
    with open(file, 'r') as f:
        content = f.read()

    # for each line in the file, add the line prefixed with the line number to the content
    lines = content.split("\n")
    for i in range(len(lines)):
        lines[i] = f"{i+1}. {lines[i]}"

    return "\n".join(lines)


projectTree = fetchProjectTree()
# print(projectTree)
# print(readFile(projectTree[0]))

# find app.tsx in the project tree
appFile = ""
for file in projectTree:
    if "App.jsx" in file:
        appFile = file
        break

# appPrompt = generatePromt("./generator/prompts/generateReplacementCode.txt", [
#     "React",
#     "App.jsx",
#     readFile(appFile),
#     "Modify the page so that every time the user clicks the button, it displays a random number between 1 and 100. Change the button text to say 'Generate Random Number'. Display the random number the paragraph element below the button.",
# ])

# open the file promptList.json
# for each prompt in the list, generate a prompt and send it to the API

with open("./generator/promptList.json", 'r') as f:
    promptList = json.load(f)

    for prompt in promptList["prompts"]:
        appPrompt = generatePrompt("./generator/prompts/generateReplacementCode.txt", [
            "React",
            "App.jsx",
            readFile(appFile),
            prompt
        ])

        response = requestGPT(client, MODEL, appPrompt)
        print(response)
        mods = parseModificationObjectsFromString(response)
        print(mods)
        modifyFile(appFile, mods)
        print("App.jsx modified successfully!")
