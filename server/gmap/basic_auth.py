import base64
import hashlib
from functools import wraps
from django.conf import settings
from django.http import HttpResponse
class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if settings.HTPASSWD:
            if not basic_auth(request):
                return unauth()
        return self.get_response(request)
def basic_auth(request):
    if "campaign.famipay" in request.path:
        return True
    if "yoyaku" in request.path:
        return True
    if "api" in request.path:
        return True
    authentication = request.META.get('HTTP_AUTHORIZATION')
    if authentication is None:
        return False
    (authmeth, auth) = authentication.split(' ', 1)
    if 'basic' != authmeth.lower():
        return False
    username, password = base64.b64decode(auth.strip()).decode().split(':', 1)
    password = '{SHA}' + base64.b64encode(hashlib.sha1(password.encode('utf-8')).digest()).decode().strip()
    if settings.HTPASSWD == username + ':' + password:
        return True
    return False
def unauth():
    response = HttpResponse(
        """<html><title>Auth required</title><body><h1>Authorization Required</h1></body></html>""",
        content_type='text/html')
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="Please enter your ID and password"'
    return response