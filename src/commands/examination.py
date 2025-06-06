import ast
import chainlit as cl
import cohere

from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate

from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable

from src.llms.cohere import command_a_03_2025
from src.prompt_engineering.examination_prompt import EXAMINATION_PROMPT


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


async def examination(message: cl.Message):
    print("[LOG] Đang sinh câu trắc nghiệm làm kiểm tra")
    user_input = message.content

    prompt = ChatPromptTemplate.from_template(template=EXAMINATION_PROMPT)
    llm = model_config()
    chain: Runnable = prompt | llm | StrOutputParser()

    exam_questions = chain.invoke(input={"question": user_input})
    print(f"[LOG] Bộ câu hỏi trắc nghiệm: {exam_questions}")

    exam_questions = ast.literal_eval(exam_questions)

    for exam_question in exam_questions:
        question = exam_question['question']
        choices = exam_question['choices']
        answer = exam_question['answer']
        if answer == "A":
            the_answer = choices[0]
        elif answer == "B":
            the_answer = choices[1]
        elif answer == "C":
            the_answer = choices[2]
        elif answer == "D":
            the_answer = choices[3]

        response = await cl.AskActionMessage(
            content=question,
            actions=[
                cl.Action(name="A", payload={"value": "A"}, label=choices[0]),
                cl.Action(name="B", payload={"value": "B"}, label=choices[1]),
                cl.Action(name="C", payload={"value": "C"}, label=choices[2]),
                cl.Action(name="D", payload={"value": "D"}, label=choices[3]),
            ],
        ).send()

        if response and response.get("payload").get("value") == str(answer):
            await cl.Message(content="✅ Chính xác!",).send()
        elif response and response.get("payload").get("value") != str(answer):
            await cl.Message(content="❌ Đáp án đúng là: " + str(the_answer) + "",).send()
    
    await cl.Message(content=f"Chúc mừng bạn hoàn thành bài thi! 😎").send()
    return