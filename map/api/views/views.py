import sys
from django.http import HttpResponse, JsonResponse
import requests
import json
import re
import time
from datetime import datetime, date, timedelta, timezone
from dateutil.relativedelta import relativedelta
import urllib.request

from bs4 import BeautifulSoup
from bs4.element import Comment
from rest_framework.views import APIView
import tweepy
import pytz

from gmap.house_model import HouseModel
from map.models import *
# from map.sqlite_models import *
from django.conf import settings
from django.core import serializers
from django.core.cache import cache
from gmap.geohash import Geohash

class CompanyAPI(APIView):

    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        companies_cache = cache.get('companies')
        if companies_cache:
            sys.getsizeof(companies_cache)
            cache.touch('companies', 30)
            return JsonResponse(companies_cache, safe=False)
        try:
            companies = session.query(Company).all()
        except Exception as e:
            print(e)
        else:
            company_dict_list = [company.to_dict() for company in companies]
            cache.set('companies', company_dict_list, 30)
        finally:
            session.close()
            return JsonResponse(company_dict_list, safe=False)

class PrefectureCityAPI(APIView):

    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        prefectures_cache = cache.get('prefectures')
        if prefectures_cache:
            sys.getsizeof(prefectures_cache)
            cache.touch('prefectures', 30)
            return JsonResponse(prefectures_cache, safe=False)
        try:
            prefectures = session.query(Prefecture).all()
        except Exception as e:
            print(e)
        else:
            prefecture_dict_list = [prefecture.with_city_dict() for prefecture in prefectures]
            cache.set('prefectures', prefecture_dict_list, 30)
        finally:
            session.close()
            return JsonResponse(prefecture_dict_list, safe=False)

class SpotAPI(APIView):
    gh = Geohash()
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    def get(self, request):
        if request.GET.dict():
            spot = self.session.query(Spot).filter(Spot.id == request.GET.dict()['id']).one_or_none()
            spot_dict = spot.join_dict()
            neighbors = self.get_neighbors(spot_dict['geohash'])
            num = 1
            while num < 6:
                stations = self.session.query(Station).filter(Station.geohash.in_(neighbors)).all()
                if stations:
                    break
                else:
                    for neighbor in neighbors:
                        neighbors = neighbors + self.get_neighbors(neighbor)
                    neighbors = list(set(neighbors))
                num += 1
            station_dict_list = [station.to_dict() for station in stations]
            spot_dict['stations'] = station_dict_list
        return JsonResponse(spot_dict, safe=False)


    def get_neighbors(self, geohash):
        neighbors = self.gh.neighbors(geohash)
        for neighbor in neighbors:
            neighbors = neighbors + self.gh.neighbors(neighbor)
        return list(set(neighbors))

class PrefectureAPI(APIView):
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    def get(self, request):
        prefectures = self.session.query(Prefecture).all()
        prefecture_dict_list = [prefecture.to_dict() for prefecture in prefectures]
        return JsonResponse(prefecture_dict_list, safe=False)

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
                print(e)
            else:
                station_dict_list = [station.to_dict() for station in stations]
            finally:
                session.close()
                return JsonResponse(station_dict_list, safe=False)
        id = request.GET.dict()['prefecture_id']
        stations_cache = cache.get(f'stations_{id}')
        if stations_cache:
            sys.getsizeof(stations_cache)
            cache.touch(f'stations_{id}', 30)
            return JsonResponse(stations_cache, safe=False)
        try:
            stations = session.query(Station).filter(Station.prefecture_id == id).all()
        except Exception as e:
            print(e)
        else:
            station_dict_list = [station.join_dict() for station in stations]
            cache.set(f'stations_{id}', station_dict_list, 30)
        finally:
            session.close()
            return JsonResponse(station_dict_list, safe=False)

class LineAPI(APIView):
    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        id = request.GET.dict()['prefecture_id']
        lines_cache = cache.get(f'lines_{id}')
        if lines_cache:
            cache.touch(f'lines_{id}', 30)
            return JsonResponse(lines_cache, safe=False)
        try:
            lines = session.query(Line).filter(Line.prefecture_id == id).all()
        except Exception as e:
            return JsonResponse({'error': e}, safe=False)
        session.close()
        line_dict_list = [line.join_dict() for line in lines]
        cache.set(f'lines_{id}', line_dict_list, 30)
        return JsonResponse(line_dict_list, safe=False)

class CityAPI(APIView):
    def get(self, request):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        id = request.GET.dict()['city_code']
        try:
            cities = session.query(City).filter(City.id == id).all()
        except Exception as e:
            print(e)
        city_dict_list = [city.to_city_dict() for city in cities]
        session.close()
        return JsonResponse(city_dict_list, safe=False)

class SearchStationAPI(APIView):
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    def get(self, request):
        word = request.GET.dict()['word']
        word = word.replace('　', ' ')
        words = word.split(' ')
        query = self.session.query(Station)
        filters = []
        for word in words:
            filters.append(and_(Station.search_text.like('%' + word + '%')))
        try:
            stations = query.filter(and_(*filters)).all()
        except Exception as e:
            print(e)
        else:
            station_dict_list = [station.join_dict() for station in stations] if stations else []
            new_station_dict_list = []
            for station_dict in station_dict_list:
                if word in station_dict['name']:
                    new_station_dict_list = [station_dict] + new_station_dict_list
                else:
                    new_station_dict_list.append(station_dict)
        return JsonResponse(new_station_dict_list, safe=False)

class SearchSpotAPI(APIView):
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    def get(self, request):
        word = request.GET.dict()['word']
        word = word.replace('　', ' ')
        words = word.split(' ')
        query = self.session.query(Town)
        filters = []
        for word in words:
            filters.append(and_(Town.address.like('%' + word + '%')))
        try:
            towns = query.filter(and_(*filters)).all()
        except Exception as e:
            print(e)
        else:
            town_dict_list = [town.to_dict() for town in towns] if towns else []
            new_town_dict_list = []
            for town_dict in town_dict_list:
                if word in town_dict['name']:
                    new_town_dict_list = [town_dict] + new_town_dict_list
                else:
                    new_town_dict_list.append(town_dict)
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
class ReverseGeocodeAPI(APIView):

    def post(self, request):
        endpoint = 'https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder?output=json&appid=' + settings.YAHOO['API_KEY'] + '&'
        dict = json.loads(request.body)
        lat = 'lat=' + str(dict['lat'])
        lng = 'lon=' + str(dict['lng'])
        query = lat + '&' + lng
        url = endpoint + query
        try:
            with requests.get(url) as response:
                data = response.json()
                data = data['Feature'][0]
                return JsonResponse(data, safe=False)
        except urllib.error.URLError as e:
            raise e.reason

class TwitterAPI(APIView):
    auth = tweepy.OAuthHandler(settings.TWITTER['API_KEY'], settings.TWITTER['API_SECRET_KEY'])
    auth.set_access_token(settings.TWITTER['ACCESS_TOKEN'], settings.TWITTER['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)
    def get(self, request):
        title = (request.GET.dict())['name']
        tweets_obj = self.api.search(title, lang='ja', rpp=80, count=100, result_type='recent', tweet_mode='extended')
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
            # tweet = {
            #     'id':  tweet_obj.id,
            #     'name':  tweet_obj.user.screen_name,
            #     'created_at':  tweet_obj.created_at,
            #     'profile_image_url': tweet_obj.user.profile_image_url,
            #     'followers_count':  tweet_obj.user.followers_count,
            #     'friends_count':  tweet_obj.user.friends_count,
            #     'text': tweet_obj.full_text,
            #     'images': images
            # }
            # tweets.append(tweet)
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

