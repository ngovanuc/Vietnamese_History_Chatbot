import chainlit as cl


commands = [
    # Command làm bài kiểm tra trắc nghiệm
    {"id":          "Examination",      # Mã định danh cho lệnh sẽ được sử dụng trong UI.
     "icon":        "book-open-check",  # Tên biểu tượng lucide cho lệnh. Xem https://lucide.dev/icons/.
     "description": "Examination",      # Mô tả lệnh.
     "button":      True,               # Có hiển thị lệnh dưới dạng nút trong trình soạn tin nhắn hay không.
     "persistent":  False},             # Có nên giữ lệnh hoạt động sau khi người dùng gửi tin nhắn hay không.
]