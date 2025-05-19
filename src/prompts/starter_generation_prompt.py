STARTER_GENERATION_PROMPT = """
Định nghĩa Starter: Starter là những prompt ngẫu nhiên ngắn gọn trong các hệ thống chatbot, giúp người dùng dễ dàng mở lời
với chatbot trong những trường hợp bí lời.

Nhiệm vụ của bạn là sinh {k} Starter ngẫu nhiên trong phạm vi Lịch sử Việt Nam một cách phong phú. Trong đó mỗi Starter bạn sinh cần có hai
trường nội dung chính, gồm: label và message. Trong đó:
    - label: là nhãn của một starter.
    - message: sẽ là prompt cho nhãn starter tương ứng.
Danh sách các starter trả về phải được đặt trong dấu ngoặc vuông: []

Dưới đây là 5 ví dụ về cấu trúc starter mà bạn sẽ phải sinh ra:
Starter 01:{{"label": "Lịch sử ngày Quốc khánh 2/9.", "message": "Hãy cho tôi biết lịch sử ngày Quốc khánh 2/9 bắt đầu từ đâu?"}}
Starter 02:{{"label": "Chuyện tình Mỵ Châu – Trọng Thủy.", "message": "Chuyện tình Mỵ Châu – Trọng Thủy là thật không?"}}
Starter 03:{{"label": "Lịch sử áo dài Việt Nam.", "message": "Lịch sử áo dài Việt Nam có từ bao giờ?"}}
Starter 04:{{"label": "Các triều đại phong kiến Việt Nam.", "message": "Có bao nhiêu triều đại phong kiến ở Việt Nam vậy?"}}
Starter 05:{{"label": "Lịch sử Thành Cổ Loa.", "message": "Thành Cổ Loa có từ thời nào? Ai xây?"}}

Không giải thích gì thêm!
"""