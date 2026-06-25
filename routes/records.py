"""签到记录查询路由"""

from flask import jsonify, session
from models import get_db, CheckinRecord
from . import records_bp


@records_bp.route('/records', methods=['GET'])
def get_records():
    """查看当前用户的签到记录（需登录）"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'msg': '请先登录'})
    
    db = get_db()
    user_id = session['user_id']
    records = db.query(CheckinRecord).filter_by(user_id=user_id) \
        .order_by(CheckinRecord.checkin_time.desc()).all()
    
    return jsonify({
        'success': True,
        'records': [{
            'id': r.id,
            'time': r.checkin_time.strftime('%Y-%m-%d %H:%M:%S'),
            'confidence': round(r.confidence, 2)
        } for r in records]
    })