from lxml import html
import requests 
import re
from lxml import etree

Days = []
from datetime import datetime, timedelta as td

Mois=['janvier','fevrier','mars','avril','mai','juin','juillet','aout','septembre','octobre','novembre','decembre']#pour obtenir les mois en francais
d1 = datetime(2010, 1, 1)
d2 = datetime.now()
delta = d2 - d1
site = 'http://www.ouest-france.fr/archives/'

for i in range(delta.days + 1):
    day_i = d1 + td(days=i)
    month = day_i.date().month
    mois_i = Mois[month-1]
    Days.append(site+day_i.strftime('%Y')+'/'+day_i.strftime('%d')+'-'+mois_i+'-'+day_i.strftime('%Y')+'/')
	
Articles = []

for i in range(0, len(Days)):
    page3=requests.get(Days[i])
    tree3 = html.fromstring(page3.content)
    liste3=tree3.xpath('//section[@class="list-t3 add-icon"]/ul/li/article/a')
    for j in range(0,len(liste3)):
        Articles.append('http://www.ouest-france.fr'+liste3[j].get("href"))
		
from tempfile import TemporaryFile
import numpy 

url = TemporaryFile()

numpy.save('url',Articles)

import pickle

with open('url', 'wb') as f:
    pickle.dump(Articles, f)

import scrapy
import pickle

with open('url', 'rb') as f:#url doit etre dans first
    my_list = pickle.load(f)

class FirstSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["ouest-france.fr"]
    start_urls = my_list

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)