from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('orders_page/', order_app),
    # path('add_message', add_message),
    # path('profile/<int:pk>', profile),
    # path('messages', messages),
    # path('', include('firstapp.urls'))
]