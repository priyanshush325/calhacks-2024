import json

from util.files import (checkPrettier, createFile, deleteFile,
                        fetchProjectTree, modifyFile, FileModification, readFile, checkFileExists, runCommandInDirectory)
from util.prompting import generatePrompt, requestGPT

# ProjectInfo type
# - projectName: str
# - projectSourceDir: str
# - repoInfoPath: str
# - repoInfo: str


class ProjectInfo:
    def __init__(self, projectName, projectSourceDir, repoInfoPath):
        self.projectName = projectName
        self.projectSourceDir = projectSourceDir
        self.repoInfoPath = repoInfoPath

        with open(repoInfoPath, 'r') as file:
            self.repoInfo = file.read()
            # print(f"Repo Info (read from .priyanshu file): {self.repoInfo}")

        # print("---------------------------------------")


# FileAction type
# - action: str "CREATE" or "MODIFY" or "DELETE"
# - filePath: str
# - contextFiles: string array
# - prompt: str


class FileAction:
    def __init__(self, action, filePath, prompt, contextFiles):
        self.action = action
        self.filePath = filePath
        self.prompt = prompt
        self.contextFiles = contextFiles

    def to_dict(self):
        return {
            "action": self.action,
            "filePath": self.filePath,
            "prompt": self.prompt,
            "contextFiles": self.contextFiles
        }



def createActionPlan(userPrompt, client, MODEL, projectInfo):

    projectTree = fetchProjectTree(projectInfo.projectSourceDir)

    prompt = generatePrompt(
        "./generator/prompts/createActionPlan.txt", [
            projectInfo.repoInfo,
            projectTree,
            userPrompt
        ])

    response = requestGPT(client, MODEL, prompt)
    commands, actions = parseActionPlan(response)

    print(f"=========COMMANDS=========")
    print("\n".join(commands))

    for action in actions:
        print(f"=========ACTION=========")
        print(f"Action: {action.action}, File: {action.filePath}")
        print(f"Prompt: {action.prompt}")
        # print(f"Context Files: {" ".join(action.contextFiles)}")

    if len(actions) == 0:
        print("No actions generated.")

    # wait for user to confirm the action plan
    print("Action plan generated. Please review the actions:")
    userString = input("Press Enter to continue or x to cancel: ")

    if "x" in userString.lower():
        print("Action plan cancelled.")
        return

    # run the commands
    for command in commands:
        runCommandInDirectory(command, projectInfo.projectSourceDir)

    # for each of the actions, grab the context files content and cache them in a dict called contextFiles
    allContextFiles = {}
    for action in actions:
        for file in action.contextFiles:
            if checkFileExists(file):
                allContextFiles[file] = readFile(file, False)

    for action in actions:
        print(f"Action: {action.action}, File: {action.filePath}")
        executeAction(action, client, MODEL, projectInfo, allContextFiles)

    print("Action plan executed successfully.")

def APIActionPlan(userPrompt, client, MODEL, projectInfo):
    projectTree = fetchProjectTree(projectInfo.projectSourceDir)

    prompt = generatePrompt(
        "./generator/prompts/createActionPlan.txt", [
            projectInfo.repoInfo,
            projectTree,
            userPrompt
        ])

    response = requestGPT(client, MODEL, prompt)
    commands, actions = parseActionPlan(response)

    action_plan = {
        "commands": commands,
        "actions": actions
    }

    return action_plan

def executeAction(action, client, MODEL, projectInfo, allContextFiles):
    if action.action == "CREATE":
        createFile(action.filePath)
    elif action.action == "DELETE":
        deleteFile(action.filePath)
        return "SUCCESS"

    contextFiles = []

    for file in action.contextFiles:
        cFS = allContextFiles.get(file, "")

        if cFS != "":
            # prepend the file name to the content and add it to the contextFiles array
            contextFiles.append(f"/* {file} */\n{cFS}")

    contextFiles = "\n".join(contextFiles)

    # now run the prompt to modify the file
    handleFeaturePrompt(action.prompt, contextFiles, action.filePath,
                        client, MODEL, projectInfo)

    return "SUCCESS"  # TODO: return "ERROR" if the file could not be modified


def parseActionPlan(string):
    actionPlan = json.loads(string)
    commands = actionPlan.get("commands", [])
    actions = []
    for action in actionPlan["actions"]:
        a = action.get("action", "MODIFY")
        fP = action.get("filePath", "")
        p = action.get("prompt", "")
        cF = action.get("contextFiles", [])

        if fP == "" or a == "":
            continue

        actions.append(FileAction(a, fP, p, cF))
    return commands, actions


def parseModificationObjectsFromString(modificationsString):

    # read the modifications object from the string
    modifications = json.loads(modificationsString)

    # the key holds "modifications" a list of dictionaries
    # convert each dictionary to a FileModification object
    modificationObjects = []
    for modification in modifications["modifications"]:
        modificationObjects.append(FileModification(
            modification.get("type", "REPLACE"),
            modification.get("startLine", 0),
            modification.get("endLine", 0),
            modification.get("code", "")
        ))

    return modificationObjects


def generateFixPrompt(file, client, MODEL, prettierInfo):
    print(f"Prettier error log was: {prettierInfo}")
    correctionPrompt = generatePrompt(
        "./generator/prompts/generateFixCode.txt", [
            "N/A",
            "N/A",
            file,
            readFile(file),
            "There was an error running prettier on the file. Here is the error log from Prettier: {prettierInfo}. Check for missing opening or closing tags, mismatched parentheses or braces, missing statements, etc. Please correct the code to fix the error."
        ])
    response = requestGPT(client, MODEL, correctionPrompt)
    mods = parseModificationObjectsFromString(response)
    result = modifyFile(file, mods)
    if result != "SUCCESS":
        return "ERROR"

    result = checkPrettier(file)

    if result == "PRETTIER_ERROR":
        return "FIX_ERROR"
    elif result == "SUCCESS":
        return "SUCCESS"


def handleFeaturePrompt(prompt, contextFiles, filePath, client, MODEL, projectInfo):

    projectTree = fetchProjectTree(projectInfo.projectSourceDir)

    appPrompt = generatePrompt(
        "./generator/prompts/generateReplacementCode.txt", [
            projectInfo.repoInfo,
            projectTree,
            contextFiles,
            filePath,
            readFile(filePath),
            prompt
        ])

    response = requestGPT(client, MODEL, appPrompt)
    mods = parseModificationObjectsFromString(response)

    for mod, i in zip(mods, range(len(mods))):
        print(f"=========MOD {i} ({mod.type})=========")
        print(f"Start: {mod.startLine}, End: {mod.endLine}")
        print(mod.code)

    result = modifyFile(filePath, mods)
    if result != "SUCCESS":
        print(f"{filePath} could not be modified.")
        return

    result = checkPrettier(filePath)

    if result[0] == "PRETTIER_ERROR":
        print("Prettier error detected. Attempting to fix...")
        result = generateFixPrompt(filePath, client, MODEL, result[2])
        if result == "SUCCESS":
            print(f"{filePath} modified successfully!")
        else:
            print(f"{filePath} could not be fixed.")
    elif result == "SUCCESS":
        print(f"{filePath} modified successfully!")


def get_latest_npm_output(WEBSERVER_OUTPUT_ABSOLUTE):
    output_lines = []
    with open(WEBSERVER_OUTPUT_ABSOLUTE, 'r') as file:
        # read the file line by line
        for line in file:
            output_lines.append(line.strip())

        # clear the file contents
        with open(WEBSERVER_OUTPUT_ABSOLUTE, 'w') as file:
            file.write("")
    return output_lines


def get_latest_error_lines(WEBSERVER_OUTPUT_ABSOLUTE):
    output_lines = get_latest_npm_output(WEBSERVER_OUTPUT_ABSOLUTE)
    error_lines = []

    for line in reversed(output_lines):
        if line_contains_error(line):
            error_lines = output_lines[output_lines.index(line):]
            break

    # remove "The above"
    if len(error_lines) > 0 and "The above" in error_lines[0]:
        line = error_lines[0]
        wordsIndex = line.find("The above")
        print("wordsIndex", wordsIndex)
        error_lines[0] = line[wordsIndex + len("The above"):]

    # if a line includes "Consider adding" then remove it and all subsequent lines
    for i, line in enumerate(error_lines):
        if "Consider adding" in line:
            error_lines = error_lines[:i]
            break

    return error_lines


def line_contains_error(line):
    if "[vite]" in line and "error" in line:
        return True
    if "above error occurred" in line:
        return True
    return False
