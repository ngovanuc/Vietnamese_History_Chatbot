SUGGESTIONS_PROMPT = """
Bạn là một chuyên gia bắt chuyện trong các hệ thống chatbot.
Nhiệm vụ của bạn là dựa vào đoạn hội thoại cuối cùng của một cuộc trò chuyện,
hãy tạo ra 03 câu hỏi gợi ý tiếp theo cùng chủ đề với câu phản hồi đó.

Câu phản hồi cuối cùng trong đoạn hội thoại như sau: {last_response}

**YÊU CẦU ĐẦU RA**:
    - Chỉ được tạo ra 03 câu hỏi gợi ý tiếp theo
    - Mỗi câu hỏi phải có cấu trúc dict như sau: {{"label": "Chủ đề câu hỏi tiếp theo", "content": "Câu hỏi dành cho chủ đề của label"}}
    - 03 câu hỏi phải được đặt trong một danh sách, ví dụ: [dict 1, dict 2, dict 3]
    - Không được phép giải thích gì thêm

Bạn có thể xem ví dụ dưới đây khi câu phản hồi cuối cùng đề cập đến cuộc đời của Hồ Chí Minh.
[
    {{"label": "Thời niên thiếu của Hồ Chí Minh", "content": "Tuổi thơ và quá trình học tập của Hồ Chí Minh diễn ra như thế nào?"}},
    {{"label": "Sự nghiệp cách mạng", "content": "Hồ Chí Minh đã hoạt động cách mạng ở những nước nào trước khi về nước lãnh đạo phong trào đấu tranh?"}},
    {{"label": "Tư tưởng Hồ Chí Minh", "content": "Tư tưởng Hồ Chí Minh có những nội dung cơ bản nào và ảnh hưởng như thế nào đến sự phát triển của Việt Nam?"}}
]
"""