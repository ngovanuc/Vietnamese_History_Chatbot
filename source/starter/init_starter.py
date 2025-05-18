import random

import chainlit as cl


def example_starter():
    label = "Đây là một ví dụ starter..."
    message = "Hãy bắt đầu một câu hỏi..."
    icon = "path\\to\\icon.svg"
    return cl.Starter(label=label, message=message, icon=icon)

async def init_starter() -> list[cl.Starter]:
    print("[LOG] Initializing starters")
    list_of_starter = [
        example_starter(),

    ]
    random_starter = random.sample(population=list_of_starter, k=1)
    return random_starter
