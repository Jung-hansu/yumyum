import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.gis.geos import GEOSGeometry
from restaurants.models import Restaurant
from utils import kakao_map_api
import csv, re

Category_id ={
    "기타":0,
    "아이스크림":800,
    "경양식":100,
    "호프":500,
    "외국음식전문점":400,
    "키즈카페":-1,
    "다방":800,
    "한식":100,
    "뷔페식":0,
    "김밥":100,
    "기타 휴게음식점":0,
    "까페":800,
    "철도역구내":-1,
    "탕류":100,
    "소주방":500,
    "일반조리판매":-1,
    "떡카페":800,
    "라이브카페":-1,
    "냉면집":100,
    "출장조리":700,
    "분식":600,
    "편의점":-1,
    "과자점":800,
    "정종":500,
    "중국식":300,
    "횟집":200,
    "푸드트럭":700,
    "패스트푸드":600,
    "백화점":-1,
    "복어취급":200,
    "식육":100,
    "통닭":100,
    "커피숍":800,
    "일식":200,
    "대포집":500,
    "패밀리레스트랑":400,
    }

def parse_category(raw_ctgr_names) -> list:
    category_ids = []
    
    pattern = r"\(.*?\)"
    category_names = re.sub(pattern, "", raw_ctgr_names)
    categories = category_names.split('/')
    for category in categories:
        c_id = Category_id.get(category, -1)
        if c_id >= 0 and not category_ids.__contains__(c_id):
            category_ids.append(c_id)
    category_ids.sort()
    return category_ids


def load_restaurants_data():
    # csv 파일 경로
    csv_path = "./Dongjak_Restaurants.csv"

    # csv 파일 읽기
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        
        try:
            # csv 데이터를 DB에 삽입
            unsaved = []
            cnt = 1
            for row in reader:
                name = row[2]
                address = row[4]
                
                category = parse_category(row[6])
                latitude, longitude = kakao_map_api.addr_to_coords(address)
                if not (category and latitude):
                    unsaved.append(row)
                    print(f"{(cnt*100/8528):.2f}% {cnt}: {name} not saved ------------------------!")
                    cnt += 1
                    continue
                location = GEOSGeometry(f"POINT({longitude} {latitude})", srid=4326)
                
                new_restaurant, created = Restaurant.objects.get_or_create(
                    name=name,
                    category=category,
                    longitude=longitude,
                    latitude=latitude,
                    location=location,
                    address=address,
                )
                new_restaurant.save()
                print(f"{(cnt*100/8528):.2f}% {cnt}: {name} saved")
                cnt += 1
                
            print("Restaurants are saved successfully.")
        except Exception: pass
        if unsaved:
            with open("./unsaved_restaurant.csv", "w") as f:
                f.write(','.join(header)+'\n')
                for row in unsaved:
                    if str(row[3]).__contains__(','):
                        row[3] = f"\"{row[3]}\""
                    f.write(','.join(row)+'\n')
            print("Unsaved restaurants:")
            print(str(unsaved).replace('],','],\n'))
        

if __name__ == "__main__":
    load_restaurants_data()
    