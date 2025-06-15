from typing import Dict, Optional
import chainlit as cl


# @cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    """
    Hàm này được gọi khi người dùng xác thực thành công qua OAuth.

    Args:
        provider_id: ID của OAuth provider (ví dụ: "github", "google").
        token: Access token từ OAuth provider.
        raw_user_data: Thông tin người dùng thô từ OAuth provider (ví dụ: email, username).
        default_user: Đối tượng cl.User mặc định.

    Returns:
        Một đối tượng cl.User nếu xác thực thành công, None nếu thất bại.
    """
    # Kiểm tra provider_id để xác định nguồn xác thực
    if provider_id == "github":
        # Xử lý thông tin người dùng từ GitHub
        # Ví dụ: lấy username từ raw_user_data
        username = raw_user_data.get("login")
        # Tạo một đối tượng cl.User mới với thông tin từ GitHub
        email = raw_user_data.get("email")  # Lấy địa chỉ email
        if username:
            user = cl.User(identifier=username, metadata={"provider": "github", "email": email})
            return user
        
        return user
    elif provider_id == "google":
        # Xử lý thông tin người dùng từ Google
        # ...
        pass
    # Nếu provider không được hỗ trợ, trả về None để từ chối xác thực
    return default_user

