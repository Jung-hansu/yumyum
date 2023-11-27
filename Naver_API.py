from config import settings
import requests

def geocoding(address):
    """
    Naver Map API - Geocoding
    
    Args:
        * address (String): 지번 주소

    Returns:
        * success -> JSON data: https://api.ncloud-docs.com/docs/ai-naver-mapsgeocoding-geocode 
        * failed  -> None
    """
    response = requests.get(
        f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}",
        headers={
            "X-NCP-APIGW-API-KEY-ID": settings.NAVER_API_KEY_ID,
            "X-NCP-APIGW-API-KEY": settings.NAVER_API_KEY,
            })
    
    if response.status_code == 200:
        return response.json()
    print(response.status_code)
    return None
