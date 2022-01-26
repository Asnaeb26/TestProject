from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('login/', login_page, name='login'),
    path('login/do_login/', do_login, name='do_login'),
    path('register/', sign_up_page, name='sign_up_page'),
    path('register/sign-up/', do_sign_up, name='do_sign_up'),
]
