from django.urls import path
from reviews.views import *

urlpatterns = [   
    path('thread/', ReviewThread.as_view()),   #스레드
]
