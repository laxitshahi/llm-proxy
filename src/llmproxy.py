import os
from models.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("GOOGLE_PROJECT_ID")


def get_completion(prompt: str) -> str:
    # Using class allows us to not worry about passing in params every time we call a function
    openai = OpenAI(prompt=prompt, api_key=openai_api_key)

    res = openai.get_completion()

    if res.err:
        return res.message

    return res.payload


def getVertexCompletion(prompt: str) -> str:
    vertex_res = vertex_ai.getAnswer(prompt)
    return vertex_res
