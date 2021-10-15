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

from django.conf import settings

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

