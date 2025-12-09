from rest_framework.permissions import BasePermission
from django.conf import settings

class APIKeyCheck(BasePermission):
    """
    Custom permission to only allow requests that provide the valid
    BUS_API_KEY in the 'X-API-Key' header.
    """
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_key_sent = request.headers.get('X-API-Key')
        server_key = getattr(settings, 'BUS_API_KEY', None)
        
        # 1. Fail Safe: If server hasn't configured a key, block everything.
        if not server_key:
            print("SECURITY WARNING: BUS_API_KEY is not set in settings. Blocking request.")
            return False

        # 2. Fail if client sent nothing
        if not api_key_sent:
            return False
        
        # 3. Standard Check
        return api_key_sent == server_key