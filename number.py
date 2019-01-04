#!/env/lib/python3
# -*- coding: utf-8 -*-
import requests
from lxml.html import fromstring
 

def getPhone(url):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
    'referer': str(url)
    }
    session = requests.session()
    resp = session.get(url, headers=headers)
 
    html = fromstring(resp.content)
    phone = html.xpath('//a[@data-marker="item-contact-bar/call"]/@href')[0]
    return phone