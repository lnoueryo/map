from django.http import HttpResponse, JsonResponse
import requests
import json
import re
import time
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

# import urllib.request
from bs4 import BeautifulSoup
from rest_framework.views import APIView

class WikiAPI(APIView):

    def get(self, request):
        print(request.GET.dict())
        title = (request.GET.dict())['name']
        url = f'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&titles={title}&rvprop=content&rvparse'
        try:
            with requests.get(url) as response:
                data = response.json()
                data = data['query']['pages']
                key = None
                for d in data:
                    key = d
                data = data[key]['revisions'][0]['*']
                data = self.disambiguation(data, request)
                data = self.parse(data)
                return HttpResponse(json.dumps(data, ensure_ascii=False))
        except requests.error as e:
            error = {'status': 404}
            return HttpResponse(json.dumps(error, ensure_ascii=False))

    def disambiguation(self, data, request):
        soup = BeautifulSoup(data, 'html.parser')
        try:
            text = soup.find('div', {'class':'mw-parser-output'}).text
            check = re.search('曖昧さ回避', text)
            if check:
                data = self.search_again(request)
        except Exception as e:
            print(e)
        finally:
            return data

    def parse(self, data):
        soup = BeautifulSoup(data, 'html.parser')
        try:
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
        except Exception as e:
            print(e)
        finally:
            return str(soup)

    def search_again(self, request):
        title = (request.GET.dict())['name'] + '_(東京都)'
        url = f'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&titles={title}&rvprop=content&rvparse'
        try:
            with requests.get(url) as response:
                page = response.json()
                page = page['query']['pages']
                key = None
                for d in page:
                    key=d
                data = page[key]['revisions'][0]['*']
        except Exception as e:
            print(e)
        finally:
            return data
