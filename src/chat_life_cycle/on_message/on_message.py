import os
import glob
import json
from typing import Dict
from typing import cast

import chainlit as cl

from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate

from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable import RunnableConfig

from langchain_cohere import ChatCohere
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from src.llms.default import default
from src.llms.cohere import command_a_03_2025
from src.llms.groq import llama3_70b_8192
from src.llms.gpt import gpt_4_32k

from src.chat_with.model_routing import model_routing

from src.prompts.question_answering import QUESTION_ANSWERING


async def on_message(message: cl.Message):
    prompt = ChatPromptTemplate.from_template(QUESTION_ANSWERING)
    llm_model = model_routing()
    chain: Runnable = prompt | llm_model | StrOutputParser()

    callback = cl.LangchainCallbackHandler()
    stream_msg = cl.Message(content="")

    user_input = message.content
    prompt_mapping = {
        "question": user_input,
    }

    if cl.user_session.get("chat_settings")["Streaming"]:
        async for chunk in chain.astream(prompt_mapping, config=RunnableConfig(callbacks=[callback])):
            await stream_msg.stream_token(chunk)
        await stream_msg.send()
    
    else:
        response = chain.invoke(
            input=prompt_mapping,
            config=RunnableConfig(callbacks=[callback])
        )
        await cl.Message(content=response).send()