from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get(settings.SIMPLE_JWT.get('ACCESS_TOKEN_COOKIE', 'access_token'))
        
        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        
            user = self.get_user(validated_token)
            
            return (user, validated_token)
            
        except (InvalidToken, TokenError) as e:
            return None