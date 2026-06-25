"""所有配置集中在这里"""

# ========== 华为云RDS配置 ==========
RDS_HOST = '你的RDS内网地址'
RDS_PORT = 3306
RDS_USER = '你的RDS用户名'
RDS_PASSWORD = '你的RDS密码'
RDS_DB = 'face_checkin'

# ========== 华为云OBS配置 ==========
OBS_ACCESS_KEY = '你的AK'
OBS_SECRET_KEY = '你的SK'
OBS_SERVER = 'obs.cn-east-3.myhuaweicloud.com'  # 根据区域修改
OBS_BUCKET = '你的桶名'

# ========== 华为云FRS配置 ==========
FRS_PROJECT_ID = '你的项目ID'
FRS_REGION = 'cn-east-3'
FACE_SET_NAME = 'face_checkin_set'

# ========== 人脸搜索配置 ==========
FACE_SEARCH_THRESHOLD = 0.85  # 置信度阈值，低于此值拒绝匹配

# ========== 上传限制 ==========
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 最大上传 10MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# ========== Flask配置 ==========
SECRET_KEY = 'your-secret-key-change-this'