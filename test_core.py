"""核心逻辑测试 —— 无需云服务，mock 所有云 SDK"""
import sys
import os
import io
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock 华为云 SDK（安装前就能跑）
sys.modules['huaweicloudsdkcore'] = MagicMock()
sys.modules['huaweicloudsdkcore.auth'] = MagicMock()
sys.modules['huaweicloudsdkcore.auth.credentials'] = MagicMock()
sys.modules['huaweicloudsdkfrs'] = MagicMock()
sys.modules['huaweicloudsdkfrs.v2'] = MagicMock()
sys.modules['huaweicloudsdkfrs.v2.region'] = MagicMock()
sys.modules['huaweicloudsdkfrs.v2.region.frs_region'] = MagicMock()
sys.modules['huaweicloudsdkfrs.v2.model'] = MagicMock()
sys.modules['boto3'] = MagicMock()
sys.modules['botocore'] = MagicMock()
sys.modules['botocore.config'] = MagicMock()
sys.modules['botocore.exceptions'] = MagicMock()

# ============================================================
# 1. 密码哈希测试
# ============================================================
from utils.auth import hash_password, verify_password

def test_password_hash():
    pw = "test123456"
    h = hash_password(pw)
    assert h != pw, "密码不应明文存储"
    assert verify_password(pw, h), "正确密码应验证通过"
    assert not verify_password("wrong", h), "错误密码应验证失败"
    h2 = hash_password(pw)
    assert h != h2, "两次哈希应产生不同结果（salted）"
    print("[PASS] 密码哈希测试通过")

# ============================================================
# 2. 照片校验测试
# ============================================================
from utils import allowed_file, validate_photo

def test_allowed_file():
    assert allowed_file("photo.jpg") == True
    assert allowed_file("photo.jpeg") == True
    assert allowed_file("photo.png") == True
    assert allowed_file("photo.JPG") == True
    assert allowed_file("photo.gif") == False
    assert allowed_file("photo") == False
    assert allowed_file("") == False
    print("[PASS] 扩展名校验测试通过")


class FakeFile:
    def __init__(self, filename, content=b''):
        self.filename = filename
        self.stream = io.BytesIO(content)


def test_validate_photo():
    # 空文件名
    valid, err = validate_photo(FakeFile(''))
    assert not valid and '照片' in err, f"空文件名应拒绝: {err}"

    # None
    valid, _ = validate_photo(None)
    assert not valid

    # 不支持格式
    valid, err = validate_photo(FakeFile('test.gif'))
    assert not valid and '格式' in err, f"不支持格式应拒绝: {err}"

    # 空文件内容
    valid, err = validate_photo(FakeFile('test.jpg', b''))
    assert not valid and '空' in err, f"空文件应拒绝: {err}"

    # 正常小文件
    valid, err = validate_photo(FakeFile('test.jpg', b'\xff\xd8\xff\xe0'))
    assert valid, f"正常文件应通过: {err}"

    # 超大文件 (>10MB)
    big = FakeFile('big.jpg')
    big.stream = io.BytesIO(b'x' * (10 * 1024 * 1024 + 1))
    valid, err = validate_photo(big)
    assert not valid and '过大' in err, f"超大文件应拒绝: {err}"

    print("[PASS] 照片校验测试通过")

# ============================================================
# 3. FRS 阈值/多脸逻辑测试（mock FRS 客户端）
# ============================================================
import utils.frs_client as frs_mod

def test_search_face_threshold_and_multiface():
    mock_client = MagicMock()

    with patch.object(frs_mod, 'get_frs_client', return_value=mock_client):
        # 场景 A：高置信度单脸 → 通过
        face_a = MagicMock()
        face_a.similarity = 0.95
        face_a.external_image_id = 'user1'
        mock_client.search_face_by_url.return_value.faces = [face_a]

        result = frs_mod.search_face('http://fake/photo.jpg', threshold=0.85)
        assert result is not None and result['username'] == 'user1'

        # 场景 B：低置信度 → 拒绝
        face_b = MagicMock()
        face_b.similarity = 0.60
        face_b.external_image_id = 'user2'
        mock_client.search_face_by_url.return_value.faces = [face_b]

        result = frs_mod.search_face('http://fake/photo.jpg', threshold=0.85)
        assert result is None, f"低置信度应拒绝: {result}"

        # 场景 C：多脸（第二张高分 → 拒绝）
        face_c1, face_c2 = MagicMock(), MagicMock()
        face_c1.similarity, face_c1.external_image_id = 0.90, 'user3'
        face_c2.similarity, face_c2.external_image_id = 0.85, 'user4'
        mock_client.search_face_by_url.return_value.faces = [face_c1, face_c2]

        result = frs_mod.search_face('http://fake/photo.jpg', threshold=0.85)
        assert result is None, f"多脸高分应拒绝: {result}"

        # 场景 D：多脸（第二张低分 → 仅最佳通过）
        face_d1, face_d2 = MagicMock(), MagicMock()
        face_d1.similarity, face_d1.external_image_id = 0.92, 'user5'
        face_d2.similarity, face_d2.external_image_id = 0.30, 'user6'
        mock_client.search_face_by_url.return_value.faces = [face_d1, face_d2]

        result = frs_mod.search_face('http://fake/photo.jpg', threshold=0.85)
        assert result is not None and result['username'] == 'user5'

        # 场景 E：无脸 → 拒绝
        mock_client.search_face_by_url.return_value.faces = []
        result = frs_mod.search_face('http://fake/photo.jpg', threshold=0.85)
        assert result is None

    print("[PASS] FRS 阈值/多脸测试通过")


# ============================================================
# 4. 输入校验规则测试
# ============================================================
def test_input_validation():
    import re

    # 用户名校验
    pat = r'^[a-zA-Z0-9_一-龥]{2,20}$'
    assert re.match(pat, 'user123')
    assert re.match(pat, '张三')
    assert not re.match(pat, 'a')
    assert not re.match(pat, 'user@name')
    assert not re.match(pat, 'a' * 21)
    assert not re.match(pat, '')
    print("[PASS] 输入校验测试通过")


if __name__ == '__main__':
    print("=" * 50)
    print("人脸签到系统 - 核心逻辑测试")
    print("=" * 50)
    test_password_hash()
    test_allowed_file()
    test_validate_photo()
    test_search_face_threshold_and_multiface()
    test_input_validation()
    print("=" * 50)
    print("全部测试通过 [PASS]")
