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


import os
import subprocess

def checkPrettier(filePath):
    # save the current directory
    originalDirectory = os.getcwd()

    # change directories into the project directory
    filePathParts = filePath.split("/")
    projectDirectory = "/".join(filePathParts[:-1])
    os.chdir(projectDirectory)
    realFilePath = filePathParts[-1]

    # run the prettier command and capture the output
    result = subprocess.run(
        ["npx", "prettier", "--write", realFilePath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # change back to the original directory
    os.chdir(originalDirectory)

    # print the output and error
    # print(f"STANDARD OUTPUT FROM PRETTIER: {result.stdout}")
    # print(f"STANDARD ERROR FROM PRETTIER: {result.stderr}")

    if result.returncode != 0:
        return "PRETTIER_ERROR", result.stdout, result.stderr
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


def createFile(filePath):
    parts = filePath.split("/")
    # recursively create the directories
    for i in range(1, len(parts)):
        path = "/".join(parts[:i])
        if not os.path.exists(path):
            os.mkdir(path)

    # create the file
    with open(filePath, 'w') as f:
        f.write("")
    return


def deleteFile(filePath):
    try:
        os.remove(filePath)
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return


def fetchProjectTree(projectDirectory):
    projectTree = []

    try:
        for root, dirs, files in os.walk(projectDirectory):
            for file in files:
                projectTree.append(os.path.join(root, file))
    except Exception as e:
        print(f"An error occurred: {e}")  # Error handling output

    # remove all files that end in .priyanshu
    projectTree = [
        file for file in projectTree if not file.endswith(".priyanshu")]

    return "\n".join(projectTree)


def readFile(file):
    content = ""
    with open(file, 'r') as f:
        content = f.read()

    if content == "":
        return f"1. /* File {file} is empty. */"

    lines = content.split("\n")
    for i in range(len(lines)):
        lines[i] = f"{i+1}. {lines[i]}"

    return "\n".join(lines)
