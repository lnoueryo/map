import time
import uuid
import hashlib
import json

import sqlalchemy as sa
from sqlalchemy.orm import backref, sessionmaker, scoped_session
from sqlalchemy import and_
from django.conf import settings
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse

from user.models import *

class UserAPI(APIView):

    def post(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        return JsonResponse(request.data, safe=False)

class Account():

    def create_session(self, user):
        salt = uuid.uuid4().hex
        session_id = hashlib.sha256(salt.encode() +  user.password.encode()).hexdigest() + ':' + salt
        session_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }
        return session_id, session_data

    def set_cookie(self, session_id, session_data):
        response = JsonResponse(session_data, safe=False)
        response.set_cookie('session_id', session_id, secure=True, samesite='Lax')
        return response

    def user_data(self, request):
        is_login = self.is_login(request)
        if is_login:
            session_id = request.COOKIES.get('session_id')
            return request.session[session_id]
        else:
            return {}

    def is_login(self, request):
        session_id = request.COOKIES.get('session_id')
        return True if session_id in request.session else False


class AuthenticationAPI(APIView):

    def login(request):
        if not request.body:
            return JsonResponse(error_response(404), safe=False)
        request_user = json.loads(request.body.decode())
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        try:
            user = session.query(User).filter(User.email == request_user['email']).one_or_none()
        except Exception as e:
            print(e)
            response = JsonResponse({'message': 'bad connection'}, safe=False)
        else:
            if user:
                password = hashlib.sha256(settings.SECRET_KEY.encode() + request_user['password'].encode()).hexdigest()
                if user.password == password:
                    session_id, session_data = account.create_session(user)
                    request.session[session_id] = session_data
                    response = account.set_cookie(session_id, session_data, secure=True, samesite='Lax')
                else:
                    response = JsonResponse({'message': 'password is wrong'}, safe=False, status=401)
            else:
                response = JsonResponse({'message': 'email is wrong'}, safe=False, status=401)
        finally:
            session.close()
        return response

    def logout(request):
        session_id = request.COOKIES.get('session_id')
        if session_id in request.session:
            del request.session[session_id]
        response = JsonResponse({'message': 'OK'}, safe=False)
        response.delete_cookie('session_id', session_id)
        return response

    def authentication(request):
        is_login = account.user_data(request)
        if any(is_login):
            return JsonResponse(is_login, safe=False, status=200)
        return JsonResponse({'message': 'not allowed to access'}, safe=False, status=403)

account = Account()

def error_response(status_code):
    if status_code == 404:
        return {'message': 'ページが見つかりませんでした。'}
    if status_code == 502:
        return {'message': '現在アクセスが集中しているため、時間をおいて再度お試しください。'}