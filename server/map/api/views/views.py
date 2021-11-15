import sys
from django.http import HttpResponse, JsonResponse
import requests
import json
from datetime import timedelta
import urllib.request
import datetime
import pytz
import logging

import sqlalchemy as sa
from sqlalchemy.orm import backref, sessionmaker, scoped_session
from sqlalchemy import and_, inspect
from bs4 import BeautifulSoup
from bs4.element import Comment
from rest_framework.views import APIView
import tweepy
from django.conf import settings
from django.core.cache import cache

from gmap.house_model import HouseModel
from map.models import *
from gmap.geohash import Geohash
from map.sqlite.views import Sqlite

sq = Sqlite()
import socket

class TableAPI(APIView):

    def get(self, request):
        try:
            inspector = inspect(engine)
            tables = []
            for table_name in inspector.get_table_names(schema='tap_map'):
                table = {'name': table_name, 'columns': [[], []]}
                for index, column in enumerate(inspector.get_columns(table_name, schema='tap_map')):
                    if index <= 12:
                        table['columns'][0].append(column['name'])
                    else:
                        table['columns'][1].append(column['name'])
                tables.append(table)
            return JsonResponse(tables, safe=False)
        except Exception as e:
            return JsonResponse(error_response(502), status=502, safe=False)
class CompanyAPI(APIView):

    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        try:
            companies = session.query(Company).all()
        except Exception  as e:
            if datetime.time(10,00,00) < datetime.datetime.now(pytz.timezone('Asia/Tokyo')).time() < datetime.time(20,00,00):
                return JsonResponse(error_response(502), status=502, safe=False)
            company_dict_list = sq.get_companies()
        else:
            company_dict_list = [company.to_join_line_station_dict() for company in companies]
        finally:
            session.close()
            response = JsonResponse(company_dict_list, safe=False)
            response.__setitem__('Cache-Control', 'public, max-age=300')
            return response
class PrefectureCityAPI(APIView):

    def get(self, request):

        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        try:
            prefectures = session.query(Prefecture).all()
        except Exception  as e:
            if datetime.time(10,00,00) < datetime.datetime.now(pytz.timezone('Asia/Tokyo')).time() < datetime.time(20,00,00):
                return JsonResponse(error_response(502), status=502, safe=False)
            prefecture_dict_list = sq.get_prefectures_cities()
        else:
            prefecture_dict_list = [prefecture.to_join_city_spot_dict() for prefecture in prefectures]
        finally:
            session.close()
            response = JsonResponse(prefecture_dict_list, safe=False)
            response.__setitem__('Cache-Control', 'public, max-age=300')
            return response

class SpotAPI(APIView):
    gh = Geohash()
    def get(self, request):
        if request.GET.dict():
            id = request.GET.dict()['id']
            Session = scoped_session(sessionmaker(bind=engine))
            session = Session()
            try:
                spot = session.query(Spot).filter(Spot.id == id).one_or_none()
            except Exception  as e:
                if datetime.time(10,00,00) < datetime.datetime.now(pytz.timezone('Asia/Tokyo')).time() < datetime.time(20,00,00):
                    return JsonResponse(error_response(502), status=502, safe=False)
                spot_dict = sq.get_spot(id)
            else:
                spot_dict = spot.to_spot_dict()
                neighbors = self.get_neighbors(spot_dict['geohash'])
                num = 1
                while num < 6:
                    try:
                        stations = session.query(Station).filter(Station.geohash.in_(neighbors)).all()
                    except Exception as e:
                        return JsonResponse(error_response(502), status=502, safe=False)
                    else:
                        if stations:
                            break
                        else:
                            for neighbor in neighbors:
                                neighbors = neighbors + self.get_neighbors(neighbor)
                            neighbors = list(set(neighbors))
                        num += 1
                station_dict_list = [station.to_join_company_line_dict() for station in stations]
                spot_dict['stations'] = station_dict_list
            finally:
                session.close()
                return JsonResponse(spot_dict, safe=False)


    def get_neighbors(self, geohash):
        neighbors = self.gh.neighbors(geohash)
        for neighbor in neighbors:
            neighbors = neighbors + self.gh.neighbors(neighbor)
        return list(set(neighbors))

class PrefectureAPI(APIView):
    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        try:
            prefectures = session.query(Prefecture).all()
        except Exception as e:
            if datetime.time(10,00,00) < datetime.datetime.now(pytz.timezone('Asia/Tokyo')).time() < datetime.time(20,00,00):
                return JsonResponse(error_response(502), status=502, safe=False)
            prefecture_dict_list = sq.get_prefectures()
        else:
            prefecture_dict_list = [prefecture.to_prefecture_dict() for prefecture in prefectures]
        finally:
            session.close()
            response = JsonResponse(prefecture_dict_list, safe=False)
            response.__setitem__('Cache-Control', 'public, max-age=300')
            return response

class StationAPI(APIView):

    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        if('name' in request.GET.dict().keys()):
            id = request.GET.dict()['prefecture_id']
            name = request.GET.dict()['name']
            try:
                stations = session.query(Station).filter(Station.prefecture_id == id).filter(Station.name == name).all()
            except Exception as e:
                if datetime.time(10,00,00) < datetime.datetime.now(pytz.timezone('Asia/Tokyo')).time() < datetime.time(20,00,00):
                    return JsonResponse(error_response(502), status=502, safe=False)
                station_dict_list = sq.get_stations_by_name(id, name)
            else:
                station_dict_list = [station.to_join_company_line_station_dict() for station in stations]
            finally:
                session.close()
                return JsonResponse(station_dict_list, safe=False)

        id = request.GET.dict()['prefecture_id']
        try:
            stations = session.query(Station).filter(Station.prefecture_id == id).all()
        except Exception as e:
            if datetime.time(10,00,00) < datetime.datetime.now(pytz.timezone('Asia/Tokyo')).time() < datetime.time(20,00,00):
                return JsonResponse(error_response(502), status=502, safe=False)
            station_dict_list = sq.get_stations(id)
        else:
            station_dict_list = [station.to_station_dict() for station in stations]
        finally:
            session.close()
            response = JsonResponse(station_dict_list, safe=False)
            response.__setitem__('Cache-Control', 'public, max-age=300')
            return response

class LineAPI(APIView):
    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        id = request.GET.dict()['prefecture_id']
        try:
            lines = session.query(Line).filter(Line.prefecture_id == id).all()
        except Exception as e:
            if datetime.time(10,00,00) < datetime.datetime.now(pytz.timezone('Asia/Tokyo')).time() < datetime.time(20,00,00):
                return JsonResponse(error_response(502), status=502, safe=False)
            line_dict_list = sq.get_lines(id)
            return JsonResponse({'error': e}, safe=False)
        else:
            line_dict_list = [line.to_line_dict() for line in lines]
        finally:
            session.close()
            response = JsonResponse(line_dict_list, safe=False)
            response.__setitem__('Cache-Control', 'public, max-age=300')
            return response

class CityAPI(APIView):
    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        id = request.GET.dict()['city_code']
        try:
            cities = session.query(City).filter(City.id == id).all()
        except Exception as e:
            if datetime.time(10,00,00) < datetime.datetime.now(pytz.timezone('Asia/Tokyo')).time() < datetime.time(20,00,00):
                return JsonResponse(error_response(502), status=502, safe=False)
            city_dict_list = sq.get_cities(id)
        else:
            city_dict_list = [city.to_join_spot_town_station_company_line_dict() for city in cities]
        finally:
            session.close()
            return JsonResponse(city_dict_list[0], safe=False)

class SearchStationAPI(APIView):
    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        word = request.GET.dict()['word']
        word = word.replace('　', ' ')
        words = word.split(' ')
        try:
            query = session.query(Station)
            filters = []
            for word in words:
                filters.append(and_(Station.search_text.like('%' + word + '%')))
            stations = query.filter(and_(*filters)).all()
        except Exception as e:
            if datetime.time(10,00,00) < datetime.datetime.now(pytz.timezone('Asia/Tokyo')).time() < datetime.time(20,00,00):
                return JsonResponse(error_response(502), status=502, safe=False)
            new_station_dict_list = sq.search_stations()
        else:
            station_dict_list = [station.to_station_dict() for station in stations] if stations else []
            new_station_dict_list = []
            for station_dict in station_dict_list:
                if word in station_dict['name']:
                    new_station_dict_list = [station_dict] + new_station_dict_list
                else:
                    new_station_dict_list.append(station_dict)
        finally:
            session.close()
            return JsonResponse(new_station_dict_list, safe=False)

class SearchSpotAPI(APIView):
    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        word = request.GET.dict()['word']
        word = word.replace('　', ' ')
        words = word.split(' ')
        try:
            query = session.query(Town)
            filters = []
            for word in words:
                filters.append(and_(Town.address.like('%' + word + '%')))
            towns = query.filter(and_(*filters)).all()
        except Exception as e:
            if datetime.time(10,00,00) < datetime.datetime.now(pytz.timezone('Asia/Tokyo')).time() < datetime.time(20,00,00):
                return JsonResponse(error_response(502), status=502, safe=False)
            new_town_dict_list = sq.search_towns(words)
        else:
            town_dict_list = [town.to_short_town_dict() for town in towns] if towns else []
            new_town_dict_list = []
            for town_dict in town_dict_list:
                if word in town_dict['name']:
                    new_town_dict_list = [town_dict] + new_town_dict_list
                else:
                    new_town_dict_list.append(town_dict)
        finally:
            session.close()
            return JsonResponse(new_town_dict_list, safe=False)

class HouseModel(APIView):

    def get(self, request):
        '''
        house_info_dict = {
            'prefecture_id': 13,
            'city_code': 102,
            'layout': '1K',
            'area': 10.16,
            'age': 24,
            'distance': 5,
            'station': '東京駅',
            'direction': '南東',
            'options': {
                'bicycle': 1,
                'bike': 0,
                'washlet': 1,
                'dryer': 1,
                'floor_heating': 0,
                'washroom': 0,
                'loft': 0,
                'furniture': 0,
                'appliance': 0,
                'autolock': 0,
            }
        }
        '''
        print(request.GET.dict())
        # house_info_dict = request.GET
        # hm = HouseModel(house_info_dict)
        # result = hm.analysis()
        return 'result'

class TwitterAPI(APIView):
    auth = tweepy.OAuthHandler(settings.TWITTER['API_KEY'], settings.TWITTER['API_SECRET_KEY'])
    auth.set_access_token(settings.TWITTER['ACCESS_TOKEN'], settings.TWITTER['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)
    def get(self, request):
        title = (request.GET.dict())['name']
        try:
            tweets_obj = self.api.search(title, lang='ja', rpp=80, count=100, result_type='recent', tweet_mode='extended')
        except Exception as e:
            return JsonResponse(error_response(502), status=502, safe=False)
        tweets = []
        for tweet_obj in tweets_obj:
            images = []
            if 'media' in tweet_obj.entities:
                images = [image['media_url'] for image in  tweet_obj.entities['media']]
            if not "RT @" in tweet_obj.full_text[0:4]:
                added_timezone = tweet_obj.created_at + timedelta(hours=9)
                tweet = {
                    'id':  tweet_obj.id,
                    'name':  tweet_obj.user.screen_name,
                    'created_at':  added_timezone,
                    'profile_image_url': tweet_obj.user.profile_image_url,
                    'followers_count':  tweet_obj.user.followers_count,
                    'friends_count':  tweet_obj.user.friends_count,
                    'text': tweet_obj.full_text,
                    'images': images
                }
                tweets.append(tweet)
        tweets = sorted(tweets, key=lambda s: s['created_at'], reverse=True)
        return JsonResponse(tweets, safe=False)


class EventAPI(APIView):

    def get(self, request):
        url = 'https://www.walkerplus.com/event_list/today/ar0313/'

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        header = {
            'User-Agent': user_agent
        }

        with requests.get(url, headers=header) as response:
            soup = BeautifulSoup(response.content, "html.parser")
            ul = soup.find('ul', {"class":"m-mainlist__list"})
            lists = ul.find_all('li', {"class":"m-mainlist__item"})
            for list in lists:
                new_lists = [s for s in list.contents if s != '\n']
                for new_list in new_lists:
                    if type(new_list) is Comment:
                        list.extract()
            imgs = ul.find_all('img')
            for img in imgs:
                img.extract()
            a_tags = soup.find_all('a')
            if a_tags:
                for a_tag in a_tags:
                    a_tag['href'] = 'https://www.walkerplus.com/' + a_tag['href']
                    a_tag['target'] = '_blank'

                return HttpResponse(ul)

def error_response(status_code):
    if status_code == 502:
        return {'message': '現在アクセスが集中しているため、時間をおいて再度お試しください。'}
        # host = socket.gethostname()
        # ip = socket.gethostbyname(host)
        # logging.warning(host)
        # logging.warning(ip)