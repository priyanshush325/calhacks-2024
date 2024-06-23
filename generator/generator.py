import json
import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI
from util.files import *
from util.prompting import *
from util.coding import *
from util.coding import ProjectInfo

load_dotenv()

parser = argparse.ArgumentParser()

parser.add_argument("directory")

args = parser.parse_args()

# print(args.directory)

client = OpenAI()
MODEL = "gpt-4o"
# PROJECT_DIRECTORY = "./frontend/src"
PROJECT_DIRECTORY = args.directory

PROJECT_INFO = ProjectInfo(
    "Calculator App", PROJECT_DIRECTORY, "./frontend/repoinfo.priyanshu")


while True:
    newPrompt = input("Add prompt: ")
    # handleFeaturePrompt(newPrompt)

    createActionPlan(newPrompt, client, MODEL, PROJECT_INFO)
