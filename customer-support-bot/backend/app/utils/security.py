import html
import re

def sanitize_input(text: str) -> str:
    """پاکسازی ورودی کاربر برای جلوگیری از حملات"""
    if not text:
        return ""
    
    # حذف تگ‌های HTML
    sanitized = html.escape(text)
    
    # حذف کاراکترهای کنترل‌کننده
    sanitized = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', sanitized)
    
    # محدودیت طول
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000]
    
    return sanitized.strip()

def validate_session_id(session_id: str) -> bool:
    """اعتبارسنجی شناسه جلسه"""
    if not session_id:
        return False
    return bool(re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$', session_id))