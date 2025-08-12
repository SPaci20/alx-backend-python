# Health check view for Django Messaging App
# Add this to your views.py or create a new health.py file

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for Kubernetes readiness and liveness probes
    """
    try:
        # Basic health check - can be expanded to check database, cache, etc.
        health_status = {
            "status": "healthy",
            "message": "Django messaging app is running",
            "service": "messaging_app"
        }
        return JsonResponse(health_status, status=200)
    except Exception as e:
        error_status = {
            "status": "unhealthy",
            "message": f"Health check failed: {str(e)}",
            "service": "messaging_app"
        }
        return JsonResponse(error_status, status=500)

# Add this to your main urls.py:
"""
from django.urls import path, include
from . import views  # or from .health import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', views.health_check, name='health_check'),  # Add this line
    # ... your other URLs
]
"""