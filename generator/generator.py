import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from util.files import *
from util.prompting import *
from util.coding import *

load_dotenv()

client = OpenAI()
MODEL = "gpt-4o"
PROJECT_DIRECTORY = "./frontend/src"


while True:
    newPrompt = input("Add prompt: ")
    # handleFeaturePrompt(newPrompt)

    createActionPlan(newPrompt, client, MODEL, PROJECT_DIRECTORY)
