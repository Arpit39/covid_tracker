
from django.urls import path
from mainapp import views

urlpatterns = [
    path("",views.home,name="home"),
    path("Country/<str:Country>/",views.cuntrylive,name="Country"),
    path("city/<str:city>/<str:Country>/<str:date>/",views.city,name="city"),
    path("news/",views.news,name="news"),
    path("newsdetails/",views.newsdetails,name="newsdetails"),
    path("newsdetails2/",views.newsdetails2,name="newsdetails2"),
]
