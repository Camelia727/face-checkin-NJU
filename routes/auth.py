"""用户认证路由"""

import re
from flask import request, jsonify, session
from models import get_db, User
from utils.obs_client import upload_to_obs
from utils.frs_client import add_face
from utils.auth import hash_password, verify_password
from utils import validate_photo
from datetime import datetime
from . import auth_bp


@auth_bp.route('/register', methods=['POST'])
def register():
    """注册：填信息 + 上传人脸照片"""
    username = (request.form.get('username') or '').strip()
    password = (request.form.get('password') or '')
    real_name = (request.form.get('real_name') or '').strip()
    photo = request.files.get('photo')

    # 表单校验
    if not all([username, password, real_name]):
        return jsonify({'success': False, 'msg': '信息不完整，请填写所有字段'})

    if not re.match(r'^[a-zA-Z0-9_一-龥]{2,20}$', username):
        return jsonify({'success': False, 'msg': '用户名需2-20位，仅支持中英文、数字和下划线'})

    if len(password) < 6:
        return jsonify({'success': False, 'msg': '密码至少需要6位'})

    if len(real_name) < 2 or len(real_name) > 20:
        return jsonify({'success': False, 'msg': '姓名需2-20个字符'})

    valid, err = validate_photo(photo)
    if not valid:
        return jsonify({'success': False, 'msg': err})

    db = get_db()

    if db.query(User).filter_by(username=username).first():
        return jsonify({'success': False, 'msg': '用户名已存在'})

    # 上传照片到OBS
    photo_data = photo.read()
    obs_key = f'faces/{username}_{int(datetime.now().timestamp())}.jpg'
    face_url = upload_to_obs(photo_data, obs_key)
    if not face_url:
        return jsonify({'success': False, 'msg': '云存储上传失败，请稍后重试'})

    # 添加到FRS人脸库
    try:
        face_id = add_face(face_url, username)
    except Exception:
        return jsonify({'success': False, 'msg': '人脸服务暂不可用，请稍后重试'})

    if not face_id:
        return jsonify({'success': False, 'msg': '未检测到人脸，请上传清晰正面照'})

    # 保存用户到数据库
    user = User(
        username=username,
        password=hash_password(password),
        real_name=real_name,
        face_url=face_url,
        face_id=face_id
    )
    db.add(user)
    db.commit()

    return jsonify({'success': True, 'msg': '注册成功'})


@auth_bp.route('/login', methods=['POST'])
def login():
    """登录"""
    username = (request.form.get('username') or '').strip()
    password = request.form.get('password') or ''

    if not username or not password:
        return jsonify({'success': False, 'msg': '请输入用户名和密码'})

    db = get_db()
    user = db.query(User).filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'msg': '用户名或密码错误'})

    if not verify_password(password, user.password):
        return jsonify({'success': False, 'msg': '用户名或密码错误'})

    session['user_id'] = user.id
    session['username'] = user.username
    return jsonify({
        'success': True,
        'msg': '登录成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'real_name': user.real_name
        }
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """注销"""
    session.clear()
    return jsonify({'success': True, 'msg': '注销成功'})


@auth_bp.route('/me', methods=['GET'])
def get_me():
    """获取当前登录用户信息"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'msg': '未登录'})

    db = get_db()
    user = db.query(User).filter_by(id=session['user_id']).first()
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'real_name': user.real_name
        }
    })
