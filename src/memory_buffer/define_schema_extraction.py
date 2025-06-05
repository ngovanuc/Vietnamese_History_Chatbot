"""Định nghĩa lược đồ trích xuất: Chỉ định những thông tin nào trong câu hỏi sẽ được trích xuất."""
from typing import Dict
from typing import List
from typing import Optional
from typing import TypedDict

from pydantic import Field
from pydantic import BaseModel


class SchemaExtractionQuestion(BaseModel):
    """A schema for extracting entities from text."""
    #  Trich xuất các thông tin đến người dùng
    name: Optional[str] = Field(..., description="Tên của người đặt câu hỏi nếu được cung cấp.")
    age_group: Optional[str] = Field(...,
                                     description="Nhóm tuổi của người đặt câu hỏi hoặc có thể suy ra được.",
                                     enum=["child", "teen", "adult", "senior"])
    language:Optional[str] = Field(...,
                                   description="Ngôn ngữ được dùng để đặt câu hỏi.",
                                   enum=["vietnamese", "english", "french", "chinese"])
    level: Optional[str] = Field(...,
                                 description="Mức độ (level) hiểu biết về lịch sử của người đặt câu hỏi (beginner: thấp, intermediate: vừa, advanced: cao)",
                                 enum=["beginner", "intermediate", "advanced"],)
    tone_preference: Optional[str] = Field(..., description="Phong cách phản hồi người dùng ưa thích, ví dụ: hài hước, nghiêm túc, thân mật, học thuật.")
    current_emotion: Optional[str] = Field(..., description="Cảm xúc hiện tại nếu có thể suy luận được, ví dụ: tò mò, buồn, vui, thất vọng.")
    
    # Trích xuất các thông tin đến câu hỏi
    current_topic: Optional[str] = Field(..., description="Chủ đề hiện tại mà người dùng đang quan tâm.")
    interested_characters: Optional[List[str]] = Field(..., description="Các nhân vật lịch sủ yêu thích của người dùng.")
    emotional_expression: Optional[str] = Field(..., description="Cảm xúc hiện tại của người dùng. Ví dụ: Eo nghe sợ vậy, Ác quá trời, Thật thú vị...")

    # Các câu hỏi không rõ ràng
    relative_question: Optional[str] = Field(..., description="Các câu hỏi có vẻ như liên quan đến chủ đề thảo luận trước đó. Ví dụ: Lúc nãy bạn nói..., Bạn có thể nói rõ hơn về vấn đề đó được không?...")
    keywords: Optional[List[str]] = Field(..., description="Các keywords quan trọng trong câu hỏi chính hoặc chủ đề cần lưu ý.")
    question_summary: Optional[str] = Field(..., description="Hãy tóm tắt lại câu hỏi (nhưng hạn chế bỏ qua các keyword kẻo mất thông tin)")


class SummaryConversation(BaseModel):
    """Một lược đồ để tóm tắt lịch sử đoạn chat."""
    # Tóm tắt lịch sử đoạn chat
    summary: Optional[str] = Field(..., description="Hãy tóm tắt lịch sử đoạn chat.")