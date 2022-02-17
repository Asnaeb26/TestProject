from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from firstapp.views import CurrentTicketView, MessagesView, UserViewSet, TicketsView

router = SimpleRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'messages', MessagesView, basename='messages')
router.register(r'tickets', TicketsView, basename='tickets')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('firstapp.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/messages/', MessagesView.as_view(), name='messages'),
    path('api/messages/<int:pk>', CurrentTicketView.as_view(), name='messages_by_ticket'),

]

urlpatterns += router.urls
