from fastapi import Request
from fastapi import Response

import chainlit as cl


# @cl.on_logout
def on_logout(request: Request, response: Response) -> None:
    response.delete_cookie("my_cookie")