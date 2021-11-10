import time
import uuid
import hashlib

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

class AccountAPI(APIView):
    def post(self, request):
        request_user = request.data
        print(request_user)
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        try:
            user = session.query(User).filter(User.email == request_user['email']).one()
        except Exception as e:
            print(e)
        else:
            password = hashlib.sha256(settings.SECRET_KEY.encode() + request_user['password'].encode()).hexdigest()
            if user.password == password:
                session_id, session_data = self.create_session(user)
                request.session[session_id] = session_data
                response = self.set_cookie(session_id, session_data)
                return response
        session.close()
        return JsonResponse(request_user, safe=False)

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
        response.set_cookie('session_id', session_id)
        return response

    def user_data(self, request):
        is_login = self.is_login(request)
        if is_login:
            session_id = request.COOKIES.get('session_id')
            return request.session[session_id]
        else:
            return

    def is_login(self, request):
        session_id = request.COOKIES.get('session_id')
        return True if session_id in request.session else False

    def logout(request):
        session_id = request.COOKIES.get('session_id')
        if session_id in request.session:
            session_data = request.session[session_id]
            response = JsonResponse(session_data, safe=False)
            response.delete_cookie('session_id', session_id)
            del request.session[session_id]
            return response
        return JsonResponse({'status': 200, 'message': 'already logged out'}, safe=False)
