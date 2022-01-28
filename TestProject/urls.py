from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from firstapp.views import *

router = SimpleRouter()

# router.register('api/users', UserView, basename='Users')
admin.site.site_header = 'Наша админка'
admin.site.index_title = 'Моя супер админка'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('firstapp.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/messages/', MessagesView.as_view(), name='messages'),
    path('api/messages/<int:pk>', CurrentMessageView.as_view(), name='messages_by_ticket'),
    path('api-auth/', include('rest_framework.urls')),

]
urlpatterns += router.urls
