from django.http import HttpResponse, JsonResponse
import requests
import json
import re
import time
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
from rest_framework.views import APIView

api_key = 'dj00aiZpPUhzbEhTY1dXWGZMaiZzPWNvbnN1bWVyc2VjcmV0Jng9ODk-'

class WikiAPI(APIView):

    def get(self, request):
        title = (request.GET.dict())['name']
        print(title)
        url = f'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&titles={title}&rvprop=content&rvparse'
        try:
            with requests.get(url) as response:
                data = response.json()
                # print(data)
                data = data['query']['pages']
                key = None
                print(data)
                for d in data:
                    key = d
                data = data[key]['revisions'][0]['*']
                data = self.disambiguation(data, request)
                data = self.parse(data)
                return HttpResponse(json.dumps(data, ensure_ascii=False))
        except urllib.error.URLError as e:
            error = {'status': 404}
            return HttpResponse(json.dumps(error, ensure_ascii=False))

    def disambiguation(self, data, request):
        soup = BeautifulSoup(data, 'html.parser')
        text = soup.find('div', {'class':'mw-parser-output'}).text
        check = re.search('曖昧さ回避', text)
        if check:
            data = self.search_again(request)
        return data

    def parse(self, data):
        soup = BeautifulSoup(data, 'html.parser')
        # print(soup.find('div', {'class':'mw-parser-output'}).text('曖昧さ回避'))
        table = soup.find('table', {"class":"box-出典の明記"})
        if table:
            table.extract()
        table = soup.find('table', {"class":"mbox-small"})
        if table:
            table.extract()
        div = soup.find('div', {"class":"mw-kartographer-container"})
        if div:
            div.extract()
        divs = soup.find_all('div', {"class":"dablink"})
        if divs:
            for div in divs:
                div.extract()
        p = soup.find('p', {"class":"mw-empty-elt"})
        if p:
            p.extract()
        infobox_table = soup.find('table', {"class":"infobox"})
        if infobox_table:
            infobox_table.find('img', {"alt":""}).extract()
        a_tags = soup.find_all('a', href=re.compile('^/wiki/'))
        if a_tags:
            for a_tag in a_tags:
                a_tag['href'] = 'https://ja.wikipedia.org' + a_tag['href']
        a_tags = soup.find_all('a', href=re.compile('^/w/'))
        if a_tags:
            for a_tag in a_tags:
                a_tag['href'] = 'https://ja.wikipedia.org' + a_tag['href']
        a_tags = soup.find_all('a')
        if a_tags:
            for a_tag in a_tags:
                a_tag['target'] = '_blank'
        return str(soup)

    def search_again(self, request):
        title = (request.GET.dict())['name'] + '_(東京都)'
        url = f'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&titles={title}&rvprop=content&rvparse'
        try:
            with requests.get(url) as response:
                data = response.json()
                data = data['query']['pages']
                key = None
                for d in data:
                    key=d
                data = data[key]['revisions'][0]['*']
                return data
        except urllib.error.URLError as e:
            print(e.reason)

class ReverseGeocodeAPI(APIView):

    def post(self, request):
        endpoint = 'https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder?output=json&appid=' + api_key + '&'
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

                # query = 'サンシャイン水族館'
                # encoded_query = urllib.parse.quote(query)
                # url = f'https://map.yahooapis.jp/search/local/V1/localSearch?output=json&appid=dj00aiZpPUhzbEhTY1dXWGZMaiZzPWNvbnN1bWVyc2VjcmV0Jng9ODk-&query={encoded_query}'

                # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
                # header = {
                #     'User-Agent': user_agent
                # }

                # with requests.get(url) as response:
                #     data = response.json()
                #     print(data['Feature'])
                return HttpResponse(ul)

    # def get(self, request):
    #     today = date.today()
    #     one_month_later = today + relativedelta(months=1) + relativedelta(months=1)
    #     today = today.strftime('%Y%m%d')
    #     print(today)
    #     one_month_later = one_month_later.strftime('%Y%m%d')
    #     url = f'https://eventon.jp/api/events.json?limit=100&prefecture_id=13&order=started_at_asc&ymd_between={today},{one_month_later}'
    #     try:
    #         with requests.get(url) as response:
    #             data = response.json()
    #             return JsonResponse(data, safe=False)
    #     except urllib.error.URLError as e:
    #         raise e.reason