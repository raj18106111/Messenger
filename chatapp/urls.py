from django.urls import path
from chatapp.views import *

urlpatterns = [
    path("",home,name='home'),
    path("room/<str:roomname>",room,name='room'),
    path("checkview",checkview,name='checkview'),
    path("friends",friends,name='friends'),
    path("removefriend",removefriend,name='removefriend'),
]
