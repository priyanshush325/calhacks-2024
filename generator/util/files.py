import json
import subprocess
import os

from pyppeteer import launch
import asyncio
from bs4 import BeautifulSoup
import errno


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


def runCommandInDirectory(command, directory):

    print(f"Running command: {command} in directory: {directory}")

    # save the current directory
    originalDirectory = os.getcwd()

    # change directories into the project directory
    os.chdir(directory)

    # run the command and capture the output
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # change back to the original directory
    os.chdir(originalDirectory)

    return result.stdout, result.stderr


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
    if not os.path.exists(os.path.dirname(filePath)):
        try:
            os.makedirs(os.path.dirname(filePath))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

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


def checkFileExists(filePath):
    return os.path.exists(filePath)


def checkIsDirectory(filePath):
    return os.path.isdir(filePath)


def readFile(file, includeLineNumbers=True):

    content = ""
    with open(file, 'r') as f:
        content = f.read()

    if content == "":
        if includeLineNumbers:
            return f"1. /* File {file} is empty. */"
        else:
            return "/* File is empty. */"

    lines = content.split("\n")
    for i in range(len(lines)):
        if includeLineNumbers:
            lines[i] = f"{i+1}. {lines[i]}"
        else:
            lines[i] = lines[i]

    return "\n".join(lines)


def readPriyanshuFile(priyanshuPath):
    with open(priyanshuPath, 'r') as f:
        data = json.load(f)
    return data


def filePathToPriyanshuPath(filePath):
    # remove everything up to the source directory
    if not "/src" in filePath:
        return ""
    relativeFilePath = filePath.split("src/")[1]

    # remove any extra spaces at the end
    relativeFilePath = relativeFilePath.strip()

    return relativeFilePath


def updatePriyanshuFile(priyanshuPath, filePath, summary):
    # read the priyanshu file
    with open(priyanshuPath, 'r') as f:
        data = json.load(f)

    relativeFilePath = filePathToPriyanshuPath(filePath)
    if relativeFilePath == "":
        return

    # if the attribute "files" is not present, add it
    if "files" not in data:
        data["files"] = {}

    # create a summary of the file
    fileSummary = summary.to_dict()

    # add the file summary to the data
    data["files"][relativeFilePath] = fileSummary

    # write the updated data back to the priyanshu file
    with open(priyanshuPath, 'w') as f:
        json.dump(data, f, indent=4)

        # # Asynchronous function to check for compile errors
        # async def checkPage(localhostLink):
        #     print(f"Checking for compile error in {localhostLink}")

        #     async def visit_link():
        #         browser = await launch(headless=True)
        #         page = await browser.newPage()
        #         await page.goto(localhostLink)
        #         # wait for selector #root
        #         await page.waitForSelector("#root")
        #         await page.waitFor(1000)
        #         content = await page.content()
        #         await browser.close()
        #         return content

        #     content = await visit_link()
        #     print(f"Content: {content}")
        #     soup = BeautifulSoup(content, 'html.parser')

        #     # find the vite-error-overlay element
        #     error_overlay = soup.find('vite-error-overlay')

        #     print(f"Error overlay: {error_overlay}")

        #     if error_overlay:
        #         print("Compile error found!")
        #         # print all the content of the error overlay
        #         print(error_overlay.)
        #         return "COMPILE_ERROR", error_overlay
        #     else:
        #         print("No compile error found!")
        #         return "SUCCESS", None

        # def checkForCompileError(localhostLink):
        #     res, error = asyncio.run(checkPage(localhostLink))
        #     return res, error
