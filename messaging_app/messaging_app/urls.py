from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views  # Import the health check view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Health check endpoint
    path('health/', views.health_check, name='health_check'),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/', include('chats.urls')),
]