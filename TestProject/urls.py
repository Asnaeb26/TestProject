from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from firstapp.views import *

router = SimpleRouter()

router.register('api/users', UserView)
# router.register('api/tickets', TicketView, basename='Tickets')
# router.register('api/tickets/messages/<int:pk>', CurrentMessageView.as_view({'get': 'list'}), basename='Mess')
# router.register('api/messages', MessagesView, basename='Messages')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('firstapp.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/messages/', MessagesView.as_view({'get': 'list'})),
    path('api/messages/<int:pk>', CurrentMessageView.as_view()),
    path('api-auth/', include('rest_framework.urls')),

]
urlpatterns += router.urls
