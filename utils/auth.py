"""用户认证相关工具"""

from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    """密码哈希（salted）"""
    return generate_password_hash(password)


def verify_password(password, password_hash):
    """验证密码"""
    return check_password_hash(password_hash, password)
