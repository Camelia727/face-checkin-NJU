"""签到路由（核心功能）"""

from flask import request, jsonify
from models import get_db, User, CheckinRecord
from utils.obs_client import upload_to_obs
from utils.frs_client import search_face
from utils import validate_photo
from datetime import datetime
from . import checkin_bp


@checkin_bp.route('/checkin', methods=['POST'])
def checkin():
    """
    人脸签到：无需登录，通过照片搜索匹配用户
    策略：多脸/低置信度均拒绝，防止误签到
    """
    photo = request.files.get('photo')

    valid, err = validate_photo(photo)
    if not valid:
        return jsonify({'success': False, 'msg': err})

    # 上传签到照片到OBS
    photo_data = photo.read()
    obs_key = f'checkin/{int(datetime.now().timestamp())}.jpg'
    photo_url = upload_to_obs(photo_data, obs_key)

    if not photo_url:
        return jsonify({'success': False, 'msg': '云存储上传失败，请稍后重试'})

    # 调用FRS搜索人脸库
    try:
        match = search_face(photo_url)
    except Exception:
        return jsonify({'success': False, 'msg': '人脸识别服务不可用，请稍后重试'})

    # 未匹配：未录入人员 或 置信度不足 或 多脸
    if match is None:
        return jsonify({'success': False, 'msg': '未识别到匹配人员，请确认已注册或使用清晰单人照'})

    # 查找对应用户
    db = get_db()
    user = db.query(User).filter_by(username=match['username']).first()
    if not user:
        return jsonify({'success': False, 'msg': '系统内部错误：用户数据不一致'})

    # 写入签到记录
    try:
        record = CheckinRecord(
            user_id=user.id,
            confidence=match['confidence'],
            photo_url=photo_url
        )
        db.add(record)
        db.commit()
    except Exception:
        return jsonify({'success': False, 'msg': '签到记录写入失败，请稍后重试'})

    return jsonify({
        'success': True,
        'msg': f'签到成功，欢迎 {user.real_name}',
        'user': {
            'name': user.real_name,
            'confidence': match['confidence']
        }
    })
