from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.db.models import Q
from restaurants.models import Restaurant
from .models import Review
from .serializers import ReviewSerializer

# Create your views here.
class ReviewListView(APIView):
    def get(self, request, restaurant_id):
        user = request.user
        if user.is_authenticated:
            if restaurant_id is not None:
                restaruant = Restaurant.objects.filter(pk = restaurant_id).first() #Restaurant 가져오기
                if not restaruant:
                    return Response({"error":"Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
                review_infos = []
                reviews = Review.objects.filter(restaurant_id = restaruant)
                for review in reviews:
                    review_info = {
                        "review_id": review.review_id,
                        "stars": review.stars,
                        "contents": review.contents,
                        "created_at": review.created_at,
                        "updated_at": review.updated_at,
                    }
                    review_infos.append(review_info)
                return Response({"ReviewList" : review_infos}, status=status.HTTP_200_OK)
            return Response({"error" : "Review not found"}, status = status.HTTP_404_NOT_FOUND)
    
class WriteReivew(APIView):   
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            restaurant_id = request.data.get('restaurant_id')
            stars = request.data.get('stars')
            contents = request.data.get('contents')
            if not (restaurant_id,stars,contents):
                return Response({"error": "평점과 리뷰 내용이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
            except Restaurant.DoesNotExist:
                return Response({"error": "레스토랑을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            Review.objects.get_or_create(user=user, restaurant=restaurant, stars=stars, contents=contents)
            return Response({"message":"Review regists successfully"}, status=status.HTTP_200_OK)
        return Response({"error":"Session expired or not found"}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteReview(APIView):
    def delete(self, request, review_id):
        user = request.user
        if user.is_authenticated:
            try:
                review = Review.objects.get(pk=review_id)
                review.delete()
                return Response({"message": "리뷰가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
            except Review.DoesNotExist:
                return Response({"error": "리뷰가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error":"Session expired or not found"}, status=status.HTTP_400_BAD_REQUEST)
        
class ReviewThread(APIView):  #thread 만들기
    def get(self, request):
        user_longitude = request.GET.get('longitude')
        user_latitude = request.GET.get('latitude')

        if not (user_longitude and user_latitude):
            return Response({"error": "잘못된 요청"}, status=status.HTTP_400_BAD_REQUEST)

        user_location = Point(float(user_longitude), float(user_latitude), srid=4326)

        # 1km 반경 안에 있는 리뷰를 가져오기
        reviews = Review.objects.annotate(
            distance=Distance('restaurant__location', user_location)
        ).filter(distance__lte=D(km=1)).order_by('created_at')
        for r in reviews:
            print(r.review_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
    """"

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
    """