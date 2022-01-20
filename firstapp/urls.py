from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('message_page/', ticket_app),
    # path('', include('firstapp.urls'))
]