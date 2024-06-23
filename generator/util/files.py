import json
import subprocess
import os

# FileModification type
# - type: str ("INSERT" or "REPLACE" or "DELETE")
# - startLine: int (inclusive)
# - endLine: int (inclusive)
# - code: str

class FileModification:
    def __init__(self, type, startLine, endLine, code):
        self.type = type
        self.startLine = startLine
        self.endLine = endLine
        self.code = code

def modifyFile(filePath, modifications):
    print(f"Printing modifications: {modifications}")

    with open(filePath, 'r') as file:
        lines = file.readlines()

    # Save the original lines (for reference/debugging, if needed)
    originalLines = lines.copy()

    # Sort modifications in reverse order based on startLine to avoid line number shifts
    modifications.sort(key=lambda x: x.startLine, reverse=True)

    for modification in modifications:
        modLines = modification.code.split("\n")
        for i in range(len(modLines)):
            modLines[i] = modLines[i] + "\n"

        if modification.type == "INSERT":
            for i in range(len(modLines)):
                lines.insert(modification.startLine - 1 + i, modLines[i])
        elif modification.type == "REPLACE":
            del lines[modification.startLine - 1:modification.endLine]
            for i in range(len(modLines)):
                lines.insert(modification.startLine - 1 + i, modLines[i])
        elif modification.type == "DELETE":
            del lines[modification.startLine - 1:modification.endLine]

    # Rewrite the file with the modifications
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

def organizeImports(filePath):
    # save the current directory
    originalDirectory = os.getcwd()

    # change directories into the project directory
    filePathParts = filePath.split("/")
    projectDirectory = "/".join(filePathParts[:-1])
    os.chdir(projectDirectory)
    realFilePath = filePathParts[-1]

    result = subprocess.run(["npx", "organize-imports-cli", realFilePath])

    # change back to the original directory
    os.chdir(originalDirectory)

    if result.returncode != 0:
        return "ORGANIZE_IMPORTS_ERROR"
    return "SUCCESS"

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
