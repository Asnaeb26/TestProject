from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from firstapp.views import MessagesViewSet, TicketsViewSet

tickets_router = SimpleRouter()
messages_router = SimpleRouter()
users_router = SimpleRouter()
tickets_router.register(r'tickets', TicketsViewSet, basename='tickets')
messages_router.register(r'messages', MessagesViewSet, basename='messages')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(tickets_router.urls)),
    path('tickets/<int:id>/', include(messages_router.urls)),

]

urlpatterns += messages_router.urls
