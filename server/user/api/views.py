import time
import uuid
import hashlib
import json
import logging

import sqlalchemy as sa
from sqlalchemy.orm import backref, sessionmaker, scoped_session
from sqlalchemy import and_
from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.http import Http404

from user.models import *
from map.models import *

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
        response.set_cookie('session_id', session_id)
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
                    response = account.set_cookie(session_id, session_data)
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

class PrefectureAPI(APIView):

    def post(self, request):
        is_login = account.user_data(request)
        request_dict = json.loads(request.body)
        if any(is_login):
            if any(request_dict):
                try:
                    prefecture = Prefecture(**request_dict)
                    validation = prefecture.validate()
                    if validation['status']:
                        Session = scoped_session(sessionmaker(bind=engine))
                        session = Session()
                        overlap = session.query(Prefecture).filter(Prefecture.id == request_dict['id']).one_or_none()
                        if overlap:
                            return JsonResponse({'message': 'id is overlapped'}, status=400, safe=False)
                        session.add(prefecture)
                        session.commit()
                        prefecture_dict = prefecture.to_prefecture_dict()
                        session.close()
                    else:
                        return JsonResponse(validation, status=400, safe=False)
                except Exception as e:
                    print(e)
                    prefecture_dict = {}
                return JsonResponse(prefecture_dict, status=201, safe=False)
            else:
                raise Http404()
        else:
            return JsonResponse({'message': 'not allowed to access'}, safe=False, status=403)

    def get(self, request):
        is_login = account.user_data(request)
        if any(is_login):
            Session = scoped_session(sessionmaker(bind=engine))
            session = Session()
            try:
                prefectures = session.query(Prefecture).all()
            except Exception as e:
                logging.error(e)
                session.close()
                return JsonResponse(error_response(502), status=502, safe=False)
            else:
                prefecture_dict_list = [prefecture.to_prefecture_dict() for prefecture in prefectures]
            finally:
                logging.info(is_login)
                session.close()
                response = JsonResponse(prefecture_dict_list, safe=False)
                response.__setitem__('Cache-Control', 'public, max-age=300')
                cache.set('prefectures', prefecture_dict_list, 600) #10分
                return response
        return JsonResponse({'message': 'not allowed to access'}, safe=False, status=403)

    def put(self, request):
        is_login = account.user_data(request)
        if any(is_login):
            Session = scoped_session(sessionmaker(bind=engine))
            session = Session()
            if 'id' in request.GET.dict():
                id = request.GET.dict()['id']
            else:
                logging.error(is_login)
                session.close()
                raise Http404()
            try:
                prefecture = session.query(Prefecture).filter(Prefecture.id == id)
            except Exception as e:
                logging.error(e)
                session.close()
                return JsonResponse(error_response(502), status=502, safe=False)
            else:
                prefecture.update(request.GET.dict())
                session.commit()
                try:
                    prefectures = session.query(Prefecture).all()
                except Exception as e:
                    logging.error(e)
                    session.close()
                    return JsonResponse(error_response(502), status=502, safe=False)
                else:
                    prefecture_dict_list = [prefecture.to_prefecture_dict() for prefecture in prefectures]
            finally:
                logging.info(is_login)
                session.close()
                response = JsonResponse(prefecture_dict_list, safe=False)
                response.__setitem__('Cache-Control', 'public, max-age=300')
                cache.set('prefectures', prefecture_dict_list, 600) #10分
                return response
        return JsonResponse({'message': 'not allowed to access'}, safe=False, status=403)
account = Account()

def error_response(status_code):
    if status_code == 404:
        return {'message': 'ページが見つかりませんでした。'}
    if status_code == 502:
        return {'message': '現在アクセスが集中しているため、時間をおいて再度お試しください。'}