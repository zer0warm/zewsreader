from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests

def _convert_time(pubDate):
    dt_obj = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S %z')
    utc_obj = datetime.utcfromtimestamp(dt_obj.timestamp())
    return utc_obj.strftime('%d/%m/%Y %H:%M:%S')

def import_sources(file):
    with open(file) as f:
        content = json.loads(f.read())
    return content['list']

def fetch_xml(url):
    resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if resp.status_code != 200:
        return 'Not good'
    return resp.text

def parse_rss(xml):
    articles = []
    soup = BeautifulSoup(xml, 'xml')
    for item in soup('item'):
        articles.append({
            'title': item.find('title').text,
            'date': _convert_time(item.find('pubDate').text),
            'url': item.find('link').text})
    return articles

def export_feeds(file, feeds):
    with open(file, 'w') as f:
        f.write(json.dumps(feeds, indent=2))

def main():
    srcs = import_sources('sources.json')
    res = {
        'title': 'Zewsfeed',
        'date': datetime.utcnow().strftime('%A, %d/%m/%Y, at %H:%M:%S'),
        'feeds': []}
    for item in srcs:
        xml = fetch_xml(item['url'])
        res['feeds'].append({
            'name': item['name'],
            'url': item['url'],
            'posts': parse_rss(xml)})
    export_feeds('feeds.json', res)

if __name__ == '__main__':
    main()
