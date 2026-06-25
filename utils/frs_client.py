"""华为云FRS人脸识别服务封装"""

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkfrs.v2 import FrsClient
from huaweicloudsdkfrs.v2.region.frs_region import FrsRegion
from huaweicloudsdkfrs.v2.model import (
    CreateFaceSetReq, FaceSet,
    AddFacesReq, AddFacesUrlReq,
    SearchFaceByUrlReq
)
from config import (
    OBS_ACCESS_KEY, OBS_SECRET_KEY, FRS_PROJECT_ID,
    FRS_REGION, FACE_SET_NAME, FACE_SEARCH_THRESHOLD
)

_frs_client = None


def get_frs_client():
    """获取FRS客户端（单例）"""
    global _frs_client
    if _frs_client is None:
        credentials = BasicCredentials(OBS_ACCESS_KEY, OBS_SECRET_KEY, FRS_PROJECT_ID)
        _frs_client = FrsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(FrsRegion.value_of(FRS_REGION)) \
            .build()
    return _frs_client


def init_face_set():
    """初始化人脸库（如果不存在则创建）"""
    client = get_frs_client()
    try:
        client.create_face_set(CreateFaceSetReq(FaceSet(name=FACE_SET_NAME)))
    except Exception:
        pass  # 已存在则忽略


def add_face(image_url, external_image_id):
    """
    添加人脸到人脸库

    Args:
        image_url: 人脸照片URL
        external_image_id: 外部标识（用用户名）

    Returns:
        str: face_id，失败返回None
    """
    client = get_frs_client()
    req = AddFacesReq(
        face_set_name=FACE_SET_NAME,
        body=AddFacesUrlReq(external_image_id=external_image_id, image_url=image_url)
    )
    resp = client.add_faces(req)
    if resp.faces and len(resp.faces) > 0:
        return resp.faces[0].face_id
    return None


def search_face(image_url, threshold=None):
    """
    在人脸库中搜索匹配的人脸

    Args:
        image_url: 待搜索的照片URL
        threshold: 置信度阈值，低于此值拒绝匹配（默认使用配置值）

    Returns:
        dict: {'username': 匹配的用户名, 'confidence': 置信度}，未匹配返回None
    """
    if threshold is None:
        threshold = FACE_SEARCH_THRESHOLD

    client = get_frs_client()
    req = SearchFaceByUrlReq(image_url=image_url)
    resp = client.search_face_by_url(FACE_SET_NAME, req)

    if not resp.faces or len(resp.faces) == 0:
        return None

    # 多脸检测：取最佳匹配
    best_match = resp.faces[0]

    # 置信度不足则拒绝
    if best_match.similarity < threshold:
        return None

    # 多脸判定：如果存在第二张高置信度人脸，说明画面不干净，拒绝签到
    if len(resp.faces) > 1:
        second_best = resp.faces[1]
        if second_best.similarity >= threshold * 0.8:
            return None

    return {
        'username': best_match.external_image_id,
        'confidence': best_match.similarity
    }
