import json

from util.files import (checkPrettier, createFile, deleteFile,
                        fetchProjectTree, modifyFile, FileModification, readFile)
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
            print(f"Repo Info: {self.repoInfo}")


# FileAction type
# - action: str "CREATE" or "MODIFY" or "DELETE"
# - filePath: str
# - prompt: str


class FileAction:
    def __init__(self, action, filePath, prompt):
        self.action = action
        self.filePath = filePath
        self.prompt = prompt


def createActionPlan(userPrompt, client, MODEL, projectInfo):

    projectTree = fetchProjectTree(projectInfo.projectSourceDir)

    prompt = generatePrompt(
        "./generator/prompts/createActionPlan.txt", [
            "React",
            projectTree,
            userPrompt
        ])

    response = requestGPT(client, MODEL, prompt)
    actions = parseActionPlan(response)

    for action in actions:
        print(f"=========ACTION=========")
        print(f"Action: {action.action}, File: {action.filePath}")
        print(f"Prompt: {action.prompt}")

    # wait for user to confirm the action plan
    print("Action plan generated. Please review the actions:")
    input("Press Enter to continue...")

    for action in actions:
        print(f"Action: {action.action}, File: {action.filePath}")
        executeAction(action, client, MODEL, projectInfo)


def executeAction(action, client, MODEL, projectInfo):
    if action.action == "CREATE":
        createFile(action.filePath)
    elif action.action == "DELETE":
        deleteFile(action.filePath)
        return "SUCCESS"

    # now run the prompt to modify the file
    handleFeaturePrompt(action.prompt, action.filePath,
                        client, MODEL, projectInfo)

    return "SUCCESS"  # TODO: return "ERROR" if the file could not be modified


def parseActionPlan(string):
    actionPlan = json.loads(string)
    actions = []
    for action in actionPlan["actions"]:
        actions.append(FileAction(
            action["action"], action["filePath"], action["prompt"]))
    return actions


def parseModificationObjectsFromString(modificationsString):

    # read the modifications object from the string
    modifications = json.loads(modificationsString)

    # the key holds "modifications" a list of dictionaries
    # convert each dictionary to a FileModification object
    modificationObjects = []
    for modification in modifications["modifications"]:
        modificationObjects.append(FileModification(
            modification["type"],
            modification["startLine"],
            modification["endLine"],
            modification["code"]
        ))

    return modificationObjects


def generateFixPrompt(file, client, MODEL, prettierInfo):
    print(f"Prettier error log was: {prettierInfo}")
    correctionPrompt = generatePrompt(
        "./generator/prompts/generateReplacementCode.txt", [
            "React",
            file,
            readFile(file),
            "There was an error running prettier on the file. Check for missing opening or closing tags, mismatched parentheses or braces, missing statements, etc. Please correct the code to fix the error. Here is the error log from Prettier: {prettierInfo}"
        ])
    response = requestGPT(client, MODEL, correctionPrompt)
    mods = parseModificationObjectsFromString(response)
    result = modifyFile(file, mods)
    if result == "SUCCESS":
        return "SUCCESS"
    else:
        return "FIX_ERROR"


def handleFeaturePrompt(prompt, filePath, client, MODEL, projectInfo):

    projectTree = fetchProjectTree(projectInfo.projectSourceDir)

    appPrompt = generatePrompt(
        "./generator/prompts/generateReplacementCode.txt", [
            projectInfo.repoInfo,
            projectTree,
            "React",
            filePath,
            readFile(filePath),
            prompt
        ])

    response = requestGPT(client, MODEL, appPrompt)
    mods = parseModificationObjectsFromString(response)

    for mod, i in zip(mods, range(len(mods))):
        print(f"=========MOD {i}=========")
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
