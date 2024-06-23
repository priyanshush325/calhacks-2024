import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from util.files import *
from util.prompting import *

load_dotenv()

client = OpenAI()
MODEL = "gpt-4o"
PROJECT_DIRECTORY = "./frontend/src"


# looks in ../frontend/src and returns a tree of all the files
def fetchProjectTree():
    projectTree = []

    try:
        for root, dirs, files in os.walk(PROJECT_DIRECTORY):
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


def addPrompt(prompt):
    with open("./generator/promptList.json", 'r') as f:
        promptList = json.load(f)

        promptList["prompts"].append(prompt)

        with open("./generator/promptList.json", 'w') as f:
            json.dump(promptList, f)

    return


def clearPrompts():
    with open("./generator/promptList.json", 'w') as f:
        json.dump({"prompts": []}, f)

    return


clearPrompts()


def generateFixPrompt(file):
    correctionPrompt = generatePrompt(
        "./generator/prompts/generateReplacementCode.txt", [
            "React",
            file,
            readFile(file),
            "There was an error running prettier on the file. Check for missing opening or closing tags, mismatched parentheses or braces, missing statements, etc. Please correct the code to fix the error."
        ])
    response = requestGPT(client, MODEL, correctionPrompt)
    mods = parseModificationObjectsFromString(response)
    result = modifyFile(file, mods)
    if result == "SUCCESS":
        return "SUCCESS"
    else:
        return "FIX_ERROR"


def handleFeaturePrompt(prompt):
    projectTree = fetchProjectTree()
    appFile = ""
    for file in projectTree:
        if "App.jsx" in file:
            appFile = file
            break

    promptObject = {
        "prompt": prompt,
        "id": "0"
    }
    print(f"Processing prompt {promptObject['id']}")
    appPrompt = generatePrompt(
        "./generator/prompts/generateReplacementCode.txt", [
            "React",
            file,
            readFile(appFile),
            promptObject["prompt"]
        ])

    response = requestGPT(client, MODEL, appPrompt)
    mods = parseModificationObjectsFromString(response)

    for mod, i in zip(mods, range(len(mods))):
        print(f"=========MOD {i}=========")
        print(f"Start: {mod.startLine}, End: {mod.endLine}")
        print(mod.code)

    result = modifyFile(appFile, mods)
    if result != "SUCCESS":
        print(f"{file} could not be modified.")
        return

    result = checkPrettier(appFile)

    if result == "PRETTIER_ERROR":
        print("Prettier error detected. Attempting to fix...")
        result = generateFixPrompt(appFile)
        if result == "SUCCESS":
            print(f"{file} modified successfully!")
        else:
            print(f"{file} could not be fixed.")
    elif result == "SUCCESS":
        print(f"{file} modified successfully!")


while True:
    newPrompt = input("Add prompt: ")
    handleFeaturePrompt(newPrompt)
