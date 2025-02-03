from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from attendance.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT Endpoints
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # App URLs
    path('api/', include('attendance.urls')),
]
