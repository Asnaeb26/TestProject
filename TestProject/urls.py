from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from firstapp.views import UserView, TicketView, UserProfileView

router = SimpleRouter()

router.register('api/users', UserView)
router.register('api/tickets', TicketView)
router.register('api/profile', UserProfileView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('firstapp.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += router.urls
