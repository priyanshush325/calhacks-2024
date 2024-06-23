import json
import os
import argparse
import glob

from dotenv import load_dotenv
from openai import OpenAI
from util.files import *
from util.prompting import *
from util.coding import *
from util.coding import ProjectInfo

load_dotenv()

parser = argparse.ArgumentParser()

parser.add_argument("directory")
parser.add_argument("port")


args = parser.parse_args()

# print(args.directory)

client = OpenAI()
MODEL = "gpt-4o"
# PROJECT_DIRECTORY = "./frontend/src"
PROJECT_SOURCE_DIRECTORY = args.directory + "/src"

#Search through Project source directory for .priyanshu file
search_pattern = os.path.join(args.directory, "*.priyanshu")

files = glob.glob(search_pattern)

if len(files) != 1:
    print("Make sure there is exactly 1 .priyanshu file in the source directory")
    exit(1)

print(f"Found .priyanshu file: {files[0]}")
print(f"Project source directory: {PROJECT_SOURCE_DIRECTORY}")
print(f"Listening on port {args.port}")
print("---------------------------------------")
INFO_PATH = files[0]


# INFO_PATH = PROJECT_SOURCE_DIRECTORY + "/repoinfo.priyanshu"

PROJECT_INFO = ProjectInfo(
    "Calculator App", PROJECT_SOURCE_DIRECTORY, INFO_PATH)


while True:
    newPrompt = input("Add prompt: ")
    # handleFeaturePrompt(newPrompt)

    createActionPlan(newPrompt, client, MODEL, PROJECT_INFO)
