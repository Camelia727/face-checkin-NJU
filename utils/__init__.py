"""工具模块"""

from config import MAX_UPLOAD_SIZE, ALLOWED_EXTENSIONS


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def validate_photo(photo):
    """校验上传照片，返回 (is_valid, error_msg)"""
    if not photo or photo.filename == '':
        return False, '请选择照片'

    if not allowed_file(photo.filename):
        return False, f'不支持的图片格式，仅支持: {", ".join(ALLOWED_EXTENSIONS)}'

    photo.stream.seek(0, 2)
    size = photo.stream.tell()
    photo.stream.seek(0)
    if size > MAX_UPLOAD_SIZE:
        return False, f'照片过大，最大允许 {MAX_UPLOAD_SIZE // (1024 * 1024)}MB'
    if size == 0:
        return False, '照片文件为空'

    return True, None
