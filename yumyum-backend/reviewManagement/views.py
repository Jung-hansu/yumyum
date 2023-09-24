from django.shortcuts import render, HttpResponse
from reviewManagement import models

# Create your views here.
def starAverage(request):
    reviews = models.Review.objects.all() # 테이블 전체 데이터 가져옴
    data = reviews.values('stars') # 그 중 stars 값만 딕셔너리형으로 가져옴

    sum = 0
    for v in data.values_list():
        sum += v
    try:
        avg = sum / data.__len__()
    except ZeroDivisionError:
        avg = 0
    return HttpResponse(avg)

def getCategory(request):
    # 카테고리 어떻게 선정할 지 논의 필요
    return HttpResponse()

def getMood(request):
    # 마찬가지
    return HttpResponse()

def inputData(request):
    # Postman 이용해서 json형식으로 데이터 입력받는 메소드
    # request respond 어케 보내는지 검색해보기
    return HttpResponse()