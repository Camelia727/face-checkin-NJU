# ========== 华为云RDS配置 ==========
RDS_HOST = '172.16.0.13'
RDS_PORT = 3306
RDS_USER = 'root'
RDS_PASSWORD = 'Camelia727.'
RDS_DB = 'face_checkin'

# ========== 华为云OBS配置 ==========
OBS_ACCESS_KEY = 'HPUAN5BPTJME7KDNL9M7'
OBS_SECRET_KEY = 'DpxD8xlOAqEjgb2utbIrVscvh9vHEY3geE2T5lQ1'
OBS_SERVER = 'obs.cn-east-3.myhuaweicloud.com'  # 根据区域修改
OBS_BUCKET = 'face-checkin'

# ========== 华为云FRS配置 ==========
FRS_PROJECT_ID = 'e89534a28c824118a34ed960ed6c66a5'
FRS_REGION = 'cn-east-3'
FACE_SET_NAME = 'face_checkin_set'

# ========== 人脸搜索配置 ==========
FACE_SEARCH_THRESHOLD = 0.85  # 置信度阈值，低于此值拒绝匹配

# ========== 上传限制 ==========
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 最大上传 10MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# ========== Flask配置 ==========
SECRET_KEY = 'your-secret-key-change-this'