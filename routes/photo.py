"""照片库管理路由（需要登录）"""

from flask import jsonify, session
from models import get_db, User
from . import photos_bp


@photos_bp.route('/photos', methods=['GET'])
def get_photos():
    """查看当前用户的人脸照片（照片库管理）"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'msg': '请先登录'})
    
    db = get_db()
    user = db.query(User).filter_by(id=session['user_id']).first()
    if not user:
        return jsonify({'success': False, 'msg': '用户不存在'})
    
    return jsonify({
        'success': True,
        'photo': {
            'face_url': user.face_url,
            'face_id': user.face_id,
            'upload_time': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None
        }
    })