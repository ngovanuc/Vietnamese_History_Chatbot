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

    Switch(id="Suggestions", label="Gợi ý chủ đề liên quan đến câu hỏi", initial=True),
    
    Slider(
        id="Temperature",
        label="Temperature",
        initial=0.5,
        min=0,
        max=1.0,
        step=0.1,
        description="Giá trị cao cho phản hồi phong phú hơn"
    ),

    Slider(
        id="Silence_threshold",
        label="Ngưỡng âm lượng.",
        initial=3500,
        min=1000,
        max=6000,
        step=100,
        description="Ngưỡng thấp cho phép thu âm thanh nhỏ hơn."
    ),

    Slider(
        id="Silence_timeout",
        label="Thời gian đợi.",
        initial=1500.0,
        min=1000,
        max=3000,
        step=100,
        description="Thời gian chờ đợi im lặng để kết thúc câu hỏi."
    ),

    Select(
        id="Voice",
        label="Chọn giọng nói",
        values=[
            "An",
            "Tâm",
            "Jessica",
            "Louis",
            "Alex",
        ],
        initial_index=0,
        description="Chọn giọng nói yêu thích."
    ),

    Slider(
        id="Voice_speed",
        label="Tốc độ phản hồi âm thanh",
        initial=180,
        min=100,
        max=300,
        step=10,
        description="Điều chỉnh tốc độ nói của chatbot."
    ),
]