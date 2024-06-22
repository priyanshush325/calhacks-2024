import json
import subprocess

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

    # run prettier on the file and check the error output ("npx", "prettier", "--write", filePath)
    result = subprocess.run(["npx", "prettier", "--write", filePath])
    if result.returncode != 0:
        print("An error occurred while running prettier on the file.")

        # # restore the original file
        # with open(filePath, 'w') as file:
        #     file.writelines(originalLines)

        return "PRETTIER_ERROR"

    return "SUCCESS"


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
