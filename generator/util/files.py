import json
import subprocess
import os

# FileModification type
# - startLine: int (inclusive)
# - endLine: int (inclusive)
# - code: str


class FileModification:
    def __init__(self, startLine, endLine, code):
        self.startLine = startLine
        self.endLine = endLine
        self.code = code


def modifyFile(filePath, modifications):

    lines = []

    with open(filePath, 'r') as file:
        lines = file.readlines()

    # save the original lines
    originalLines = lines.copy()

    for modification in modifications:

        modLines = modification.code.split("\n")
        for i in range(len(modLines)):
            modLines[i] = modLines[i] + "\n"

        # remove the lines that are being replaced
        del lines[modification.startLine - 1:modification.endLine]

        # insert the new lines
        for i in range(len(modLines)):
            lines.insert(modification.startLine - 1 + i, modLines[i])

    # rewrite the file with the modifications
    with open(filePath, 'w') as file:
        file.writelines(lines)

    return "SUCCESS"


def checkPrettier(filePath):

    # save the current directory
    originalDirectory = os.getcwd()

    # change directories into the project directory
    filePathParts = filePath.split("/")
    projectDirectory = "/".join(filePathParts[:-1])
    os.chdir(projectDirectory)
    realFilePath = filePathParts[-1]

    result = subprocess.run(["npx", "prettier", "--write", realFilePath])

    # change back to the original directory
    os.chdir(originalDirectory)

    if result.returncode != 0:
        return "PRETTIER_ERROR"
    return "SUCCESS"


# def organizeImports(filePath):
#     # save the current directory
#     originalDirectory = os.getcwd()

#     # change directories into the project directory
#     filePathParts = filePath.split("/")
#     projectDirectory = "/".join(filePathParts[:-1])
#     os.chdir(projectDirectory)
#     realFilePath = filePathParts[-1]

#     result = subprocess.run(["npx", "organize-imports-cli", realFilePath])

#     # change back to the original directory
#     os.chdir(originalDirectory)

#     if result.returncode != 0:
#         return "ORGANIZE_IMPORTS_ERROR"
#     return "SUCCESS"


def parseModificationObjectsFromString(modificationsString):

    # read the modifications object from the string
    modifications = json.loads(modificationsString)

    # the key holds "modifications" a list of dictionaries
    # convert each dictionary to a FileModification object
    modificationObjects = []
    for modification in modifications["modifications"]:
        modificationObjects.append(FileModification(
            modification["startLine"],
            modification["endLine"],
            modification["code"]
        ))

    return modificationObjects
