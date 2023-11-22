import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.gis.geos import GEOSGeometry
from restaurants.models import Restaurant
from Naver_API import geocoding
import csv, re

Category_id ={
    "기타":0,
    "아이스크림":100,
    "경양식":200,
    "업태명":300,
    "호프":400,
    "외국음식전문점":500,
    "키즈카페":600,
    "다방":700,
    "한식":800,
    "뷔페식":900,
    "김밥":1000,
    "기타 휴게음식점":1100,
    "까페":1200,
    "철도역구내":1300,
    "탕류":1400,
    "소주방":1500,
    "일반조리판매":1600,
    "떡카페":1700,
    "라이브카페":1800,
    "냉면집":1900,
    "출장조리":2000,
    "분식":2100,
    "편의점":2200,
    "과자점":2300,
    "정종":2400,
    "중국식":2500,
    "횟집":2600,
    "푸드트럭":2700,
    "패스트푸드":2800,
    "백화점":2900,
    "복어취급":3000,
    "식육":3100,
    "통닭":3200,
    "커피숍":3300,
    "일식":3400,
    "대포집":3500,
    "패밀리레스트랑":3600,
    }

def parse_category(raw_ctgr_names) -> list:
    category_ids = []
    
    pattern = r"\(.*?\)"
    category_names = re.sub(pattern, "", raw_ctgr_names)
    categories = category_names.split('/')
    for category in categories:
        category_ids.append(Category_id[category])
        
    return category_ids


def load_restaurants_data():
    # csv 파일 경로
    csv_path = "./Dongjak_Restaurants.csv"

    # csv 파일 읽기
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        
        # Skip header
        next(reader, None)
        
        # csv 데이터를 DB에 삽입
        cnt = 0
        for row in reader:
            cnt += 1
            name = row[2]
            category = parse_category(row[6])
            
            address = row[4]
            api_response = geocoding(address)
            if not api_response:
                return print("Geocoding error")
            api_addresses = api_response.get('addresses')
            if not api_addresses:
                print(f"{cnt}: {name} not saved.")
                continue
            longitude = api_addresses[0].get('x')
            latitude = api_addresses[0].get('y')
            location = GEOSGeometry(f"POINT({float(longitude)} {float(latitude)})", srid=4326)
            
            new_restaurant, create = Restaurant.objects.get_or_create(
                name=name,
                category=category,
                longitude=longitude,
                latitude=latitude,
                location=location,
                address=address,
                )
            new_restaurant.save()
            print(f"{cnt}: {name} saved.")
        print("All restaurants are saved successfully.")
        

if __name__ == "__main__":
    load_restaurants_data()