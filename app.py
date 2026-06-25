"""Flask应用主入口"""

from flask import Flask, render_template
from flask_cors import CORS
from config import SECRET_KEY
from models import init_db
from utils.frs_client import init_face_set
from routes import auth_bp, checkin_bp, records_bp, photos_bp

# 创建Flask应用
app = Flask(__name__)
app.secret_key = SECRET_KEY

# 跨域支持
CORS(app, supports_credentials=True)

# 初始化数据库和人脸库
init_db()
init_face_set()

# 注册蓝图
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(checkin_bp, url_prefix='/api')
app.register_blueprint(records_bp, url_prefix='/api')
app.register_blueprint(photos_bp, url_prefix='/api')

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)