import chainlit as cl
from chainlit.input_widget import Select
from chainlit.input_widget import Switch
from chainlit.input_widget import Slider


chat_settings = [
    Select(
        id="Model",
        label="Chọn mô hình",
        values=[
            "base_model",
            "command-a-03-2025",
            "llama3-70b-8192",
            "gemini-2.0-flash",
            "claude-3-7-sonnet-20250219",
            "mistral-large-latest",
            "gpt-3.5-turbo (alpha)",
        ],
        initial_index=0,
    ),

    Switch(id="Streaming", label="Phản hồi tức thì", initial=True),
    
    Slider(
        id="Temperature",
        label="Temperature",
        initial=0.5,
        min=0,
        max=1.0,
        step=0.1,
        description="Giá trị cao cho phản hồi phong phú hơn"
    ),
]