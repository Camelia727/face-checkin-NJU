"""数据库模型定义 - SQLAlchemy 1.4 兼容版本"""

from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from datetime import datetime
from config import RDS_HOST, RDS_PORT, RDS_USER, RDS_PASSWORD, RDS_DB

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    real_name = Column(String(50))
    face_url = Column(String(500))
    face_id = Column(String(100))
    created_at = Column(TIMESTAMP, default=datetime.now)


class CheckinRecord(Base):
    __tablename__ = 'checkin_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    checkin_time = Column(TIMESTAMP, default=datetime.now)
    confidence = Column(Float)
    photo_url = Column(String(500))


# 创建数据库引擎（带连接池）
engine = create_engine(
    f'mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DB}?charset=utf8mb4',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
    echo=False
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 线程安全的会话
db_session = scoped_session(SessionLocal)


def init_db():
    """初始化数据库（建表）"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话（用于请求上下文）"""
    return db_session()