"""路由模块"""
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
checkin_bp = Blueprint('checkin', __name__)
records_bp = Blueprint('records', __name__)
photos_bp = Blueprint('photos', __name__)  # 新增

from . import auth, checkin, records, photos