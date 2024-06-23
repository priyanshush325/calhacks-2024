import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from util.files import *
from util.prompting import *
from util.coding import *
from util.coding import ProjectInfo

load_dotenv()

client = OpenAI()
MODEL = "gpt-4o"
PROJECT_DIRECTORY = "./frontend/src"

PROJECT_INFO = ProjectInfo(
    "Calculator App", "./frontend/src", "./frontend/repoinfo.priyanshu")


while True:
    newPrompt = input("Add prompt: ")
    # handleFeaturePrompt(newPrompt)

    createActionPlan(newPrompt, client, MODEL, PROJECT_INFO)
