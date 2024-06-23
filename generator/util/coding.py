import json

from util.files import *
from util.prompting import generatePrompt, requestGPT
import threading

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

        priyanshuFile = readPriyanshuFile(repoInfoPath)
        self.repoInfo = priyanshuFile.get("description", {})

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

    actionPlan = APIActionPlan(userPrompt, client, MODEL, projectInfo, [])
    commands = actionPlan["commands"]
    actions = actionPlan["actions"]

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

    confirmActions(actions, client, MODEL, projectInfo)


def APIActionPlan(userPrompt, client, MODEL, projectInfo, promptHistory):
    projectTree = fetchProjectTree(projectInfo.projectSourceDir)

    NUM_HISTORY = 3
    lastTwoPrompts = promptHistory[-NUM_HISTORY:]
    lastTwoPrompts = "\n".join(
        [f"{i + 1}. {p}" for i, p in enumerate(lastTwoPrompts)])

    print("APIActionPlan: ", userPrompt)
    # print cwd
    print("CWD: ", os.getcwd())

    # fetch file information from project tree and .priyanshu file
    priyanshuFile = readPriyanshuFile(projectInfo.repoInfoPath)
    projectTree = projectTree.split("\n")
    projectFiles = []
    for file in projectTree:
        fileDetails = getPriyanshuFileFileDetails(file, priyanshuFile)
        if fileDetails is not None:
            projectFiles.append(fileDetails)
        else:
            projectFiles.append(file)

    projectTreeWithInfo = "\n".join(projectFiles)

    prompt = generatePrompt(
        "./generator/prompts/createActionPlan.txt", [
            projectInfo.repoInfo,
            projectTreeWithInfo,
            lastTwoPrompts,
            userPrompt
        ])

    response = requestGPT(client, MODEL, prompt)
    commands, actions = parseActionPlan(response)

    action_plan = {
        "commands": commands,
        "actions": actions
    }

    return action_plan


def confirmActions(actionPlan, client, MODEL, projectInfo):

    print("PENDING_ACTIONS: ", actionPlan)
    if actionPlan is None:
        return "No actions found", 400
    else:
        print("running commands")
        # run the commands
        for command in actionPlan["commands"]:
            print(f"Running command: {command}")
            runCommandInDirectory(command, projectInfo.projectSourceDir)

        # Execute actions

        print("running actions")
        allContextFiles = {}
        for action in actionPlan["actions"]:
            for file in action.contextFiles:
                if checkFileExists(file):
                    allContextFiles[file] = readFile(file, False)
        for action in actionPlan["actions"]:
            # print(f"Action: {action.action}, File: {
            #       action.filePath}, Prompt: {action.prompt}")
            print(f"Running action: {action.action} {action.filePath}")
            executeAction(action, client, MODEL, projectInfo, allContextFiles)

    # spawn another process to update the summary
    # new thread
    try:
        if len(actionPlan.get("actions", [])) > 0:
            updateSummaryThread = threading.Thread(
                target=updateSummary, args=(actionPlan["actions"], client, MODEL, projectInfo))
            updateSummaryThread.start()
    except Exception as e:
        print(f"An error occurred while trying to update the summary: {e}")

    return "Actions executed", 200


def updateSummary(actions, client, MODEL, projectInfo):
    print("Updating summary...")

    for action in actions:
        if (action.action == "MODIFY" or action.action == "CREATE"):
            summary = summarizeFile(action.filePath, client, MODEL)
            updatePriyanshuFile(projectInfo.repoInfoPath,
                                action.filePath, summary)

    print("Summary updated successfully.")


def resummariesFiles(client, MODEL, projectInfo):
    projectTree = fetchProjectTree(projectInfo.projectSourceDir)
    projectTree = projectTree.split("\n")
    for file in projectTree:
        print(f"Resummarizing file: {file}")
        summary = summarizeFile(file, client, MODEL)
        if summary is None:
            print(f"Could not resummarize {file}.")
            continue
        print(f"Summary: {summary.description}")
        updatePriyanshuFile(projectInfo.repoInfoPath, file, summary)

    print("All files resummarized.")


def executeAction(action, client, MODEL, projectInfo, allContextFiles):
    if action.action == "CREATE":
        print(f"Creating file: {action.filePath}")
        createFile(action.filePath)
    elif action.action == "DELETE":
        deleteFile(action.filePath)
        return "SUCCESS"

    contextFiles = []

    for file in action.contextFiles:
        try:
            cFS = readFile(file, False)

            if cFS != "":
                # prepend the file name to the content and add it to the contextFiles array
                contextFiles.append(f"/* {file} */\n{cFS}")
        except Exception as e:
            print("Trying to read file from allContextFiles.")
            try:
                cFS = allContextFiles.get(file, "")
                if cFS != "":
                    # prepend the file name to the content and add it to the contextFiles array
                    contextFiles.append(f"/* {file} */\n{cFS}")
            except Exception as e2:
                print(f"Could not read file {file}.")

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

    print("Checking prettier again...")

    result = checkPrettier(file)

    print(f"HEREHEHE Result: {result}")
    print(result[0])

    if result[0] == "PRETTIER_ERROR":
        print("Prettier error 2 detected. Attempting to fix...")
        result = generateLastDitchFixPrompt(
            file, client, MODEL, result[2])
        if result == "ERROR":
            return "ERROR"
        elif result == "SUCCESS":
            return "SUCCESS"
    elif result == "SUCCESS":
        print("Prettier error fixed successfully (1)")
        return "SUCCESS"
    else:
        return "ERROR"


def generateLastDitchFixPrompt(file, client, MODEL, prettierInfo):
    correctionPrompt = generatePrompt(
        "./generator/prompts/generateFixCode.txt", [
            "N/A",
            "N/A",
            file,
            readFile(file),
            "Rewrite the entire file. Make sure to include all necessary imports, exports, and other required code. Make sure the new file is syntactically correct."
        ])
    response = requestGPT(client, MODEL, correctionPrompt)
    mods = parseModificationObjectsFromString(response)
    result = modifyFile(file, mods)
    if result != "SUCCESS":
        return "ERROR"


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

# summary
# - description: str
# - exports: str[]
# - imports: str[]


class Summary:
    def __init__(self, description, exports, imports):
        self.description = description
        self.exports = exports
        self.imports = imports

    def to_dict(self):
        return {
            "description": self.description,
            "exports": self.exports,
            "imports": self.imports
        }


def summarizeFile(filePath, client, MODEL):

    # check if the file exists and is a file not a directory
    if not checkFileExists(filePath) or checkIsDirectory(filePath):
        return None

    # read the file
    fileContent = readFile(filePath)
    summaryPrompt = generatePrompt(
        "./generator/prompts/summarizeFile.txt", [
            filePath,
            fileContent
        ])

    response = requestGPT(client, "gpt-3.5-turbo", summaryPrompt)

    summary = parseSummaryResponse(response)

    return summary


def parseSummaryResponse(response):
    summary = json.loads(response)
    description = summary.get("description", "")
    exports = summary.get("exports", [])
    imports = summary.get("imports", [])
    return Summary(description, exports, imports)
