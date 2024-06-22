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


def handlePrompt(prompt):
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

    # with open("./generator/promptList.json", 'r') as f:
    #     promptList = json.load(f)

    #     promptObjectList = []
    #     i = 0
    #     for prompt in promptList["prompts"]:
    #         # add an object to the list with the prompt and the status
    #         promptObjectList.append({
    #             "prompt": prompt,
    #             "status": "PENDING",
    #             "id": f"{i}"
    #         })
    #         i += 1

    #     while True:
    #         # find the first prompt that is pending
    #         promptObject = None
    #         for pO in promptObjectList:
    #             if pO["status"] == "PENDING":
    #                 promptObject = pO
    #                 break

    #         if promptObject is None:
    #             print("All prompts have been completed.")
    #             break

    #         promptObject["status"] = "IN_PROGRESS"

    promptObject = {
        "prompt": prompt,
        "id": "0"
    }
    print(f"Processing prompt {promptObject['id']}")
    appPrompt = generatePrompt(
        "./generator/prompts/generateReplacementCode.txt", [
            "React",
            "App.jsx",
            readFile(appFile),
            promptObject["prompt"]
        ])

    response = requestGPT(client, MODEL, appPrompt)
    print("=====================================")
    print(response)
    print("=====================================")
    mods = parseModificationObjectsFromString(response)
    result = modifyFile(appFile, mods)
    if result == "PRETTIER_ERROR":

        print("Prettier error number 1")

        correctionPrompt = generatePrompt(
            "./generator/prompts/generateReplacementCode.txt", [
                "React",
                "App.jsx",
                readFile(appFile),
                "There was an error running prettier on the file. Check for missing opening or closing tags, missing statements, etc. Please correct the code to fix the error."
            ])

        response = requestGPT(client, MODEL, correctionPrompt)
        mods = parseModificationObjectsFromString(response)
        newResult = modifyFile(appFile, mods)
        if newResult == "PRETTIER_ERROR":
            print("Prettier error number 2")
            return
        else:
            print("App.jsx fixed successfully!")
            promptObject["status"] = "COMPLETE"
    elif result == "SUCCESS":
        print("App.jsx modified successfully!")

        # for prompt in promptList["prompts"]:
        #     appPrompt = generatePrompt("./generator/prompts/generateReplacementCode.txt", [
        #         "React",
        #         "App.jsx",
        #         readFile(appFile),
        #         prompt
        #     ])

        #     response = requestGPT(client, MODEL, appPrompt)
        #     print(response)
        #     mods = parseModificationObjectsFromString(response)
        #     print(mods)
        #     result = modifyFile(appFile, mods)
        #     if result == "RETRY":

        #         break
        #     print("App.jsx modified successfully!")


while True:
    # clearPrompts()
    newPrompt = input("Add prompt:")

    # addPrompt(newPrompt)
    handlePrompt(newPrompt)

    # choice = input("Add another prompt? (y/n): ")
    # if choice.lower() != 'y':
    #     break

    # addPrompt(input("Add prompt: "))
