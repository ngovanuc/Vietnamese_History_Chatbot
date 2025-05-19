import ast
import random
import cohere
import chainlit as cl

from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate

from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable import RunnableConfig

from src.llms.cohere import command_a_03_2025
from src.prompts.starter_generation_prompt import STARTER_GENERATION_PROMPT


llm = command_a_03_2025()
model_name = llm.model_name
api_key = llm.api_key

co = cohere.Client(api_key=api_key)

def model_config():
    model_config = ChatCohere(
        model=model_name,
        cohere_api_key=api_key,
        streaming=False,
        temperature=1.0,
    )
    return model_config

def generating_starters(k=5) -> str:
    prompt = ChatPromptTemplate.from_template(template=STARTER_GENERATION_PROMPT)
    llm = model_config()
    chain: Runnable = prompt | llm | StrOutputParser()

    prompt_mapping = {
        "k": k,
    }
    string_starters = chain.invoke(input=prompt_mapping)
    return string_starters

def string_starters_to_dict(string_starters: str) -> dict:
    dict_starters = ast.literal_eval(string_starters)
    return dict_starters
    
# @cl.set_starters
async def set_starters() -> list[cl.Starter]:
    print("[LOG] Initializing starters")
    k = random.randint(2, 6)
    string_starters = generating_starters(k=k)
    list_dict_starters = string_starters_to_dict(string_starters=string_starters)

    starters = []
    for dict_starter in list_dict_starters:
        label = dict_starter["label"]
        message = dict_starter["message"]
        icon = "path\\to\\icon.svg"
        starters.append(cl.Starter(label=label, message=message))
    return starters