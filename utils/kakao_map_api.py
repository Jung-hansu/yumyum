from config import settings
import requests


def search_addr(addr):
    """
    Kakao Map API - 주소 검색
    
    Args:
        * address (String): 지번 주소

    Returns:
        * success -> JSON data: https://developers.kakao.com/docs/latest/ko/local/dev-guide#address-coord-response-body-document
        * failed  -> None
    """
    request = requests.get(
        f"https://dapi.kakao.com/v2/local/search/address.json?query={addr}",
        headers = {"Authorization": f"KakaoAK {settings.KAKAO_API_KEY}"}
    )
    
    if request.status_code == 200:
        return request.json()
    print(request.status_code)
    return None

def addr_to_coords(addr):
    """
    Kakao Map API - 주소를 좌표로 변환
    
    Args:
        * address (String): 지번 주소

    Returns:
        * success -> lon, lat data: https://developers.kakao.com/docs/latest/ko/local/dev-guide#address-coord-response-body-document
        * failed  -> None
    """
    result = search_addr(addr)
    if not result or not result["documents"]:
        return None, None
    address = result["documents"][0]["address"]
    return float(address["x"]), float(address["y"])