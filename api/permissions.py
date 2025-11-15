from rest_framework.permissions import BasePermission
from django.conf import settings

class APIKeyCheck(BasePermission):
    message = 'Invalid/Missing API Key'
    def check(self, request, view):
        api_key_sent = request.headers.get('X-API-Key')

        return api_key_sent == settings.BUS_API_KEY