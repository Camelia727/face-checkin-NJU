"""OBS对象存储操作封装 - 使用 boto3 (S3兼容协议)"""

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from config import OBS_ACCESS_KEY, OBS_SECRET_KEY, OBS_SERVER, OBS_BUCKET

# OBS 的 S3 兼容端点
S3_ENDPOINT = f'https://{OBS_SERVER}'

_s3_client = None


def get_s3_client():
    """获取 S3 客户端（单例）"""
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            's3',
            aws_access_key_id=OBS_ACCESS_KEY,
            aws_secret_access_key=OBS_SECRET_KEY,
            endpoint_url=S3_ENDPOINT,
            region_name='cn-east-3',
            config=Config(
                signature_version='s3v4',
                retries={'max_attempts': 3}
            )
        )
    return _s3_client


def upload_to_obs(data, key):
    """
    上传二进制数据到OBS
    
    Args:
        data: 二进制数据
        key: OBS中的文件路径
    
    Returns:
        str: 文件的公网访问URL，失败返回None
    """
    try:
        client = get_s3_client()
        client.put_object(
            Bucket=OBS_BUCKET,
            Key=key,
            Body=data
        )
        return f'https://{OBS_BUCKET}.{OBS_SERVER}/{key}'
    except ClientError as e:
        print(f"OBS上传失败: {e}")
        return None