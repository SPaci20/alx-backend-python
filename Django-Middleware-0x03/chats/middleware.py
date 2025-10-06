import datetime
import os
from django.conf import settings

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Ensure the log file directory exists
        log_dir = os.path.dirname(settings.REQUEST_LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        
        # Get user information
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        
        # Create log entry
        log_entry = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}\n"
        
        # Write to log file
        try:
            with open(settings.REQUEST_LOG_FILE, 'a') as log_file:
                log_file.write(log_entry)
        except Exception as e:
            # If logging fails, print to console as fallback
            print(f"Failed to write to log file: {e}")
            print(log_entry.strip())
        
        return response