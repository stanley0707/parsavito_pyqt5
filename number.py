import requests
from urllib.parse import urljoin
 
from lxml.html import fromstring
 
def getPhone(url):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
    'referer': "https://m.avito.ru/feodosiya/kvartiry/2-k_kvartira_42_m_25_et._1288913835"
    }
    session = requests.session()
    resp = session.get(url, headers=headers)
 
    html = fromstring(resp.content)
    phone = html.xpath('//a[@data-marker="item-contact-bar/call"]/@href')[0]
    return phone