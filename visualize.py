from bs4 import BeautifulSoup
import json

def make_feed_section(soup, section, feed):
    soup.new_tag('h2')
    section.append(soup.new_tag('h2'))
    section.h2.append(soup.new_tag('a', href=feed['url']))
    section.h2.a.append(feed['name'])
    section.append(soup.new_tag('ul'))
    for post in feed['posts']:
        li = soup.new_tag('li')
        li.append(f"[{post['date']}] ")
        li.append(soup.new_tag('a', href=post['url']))
        li.a.append(post['title'])
        section.ul.append(li)

def main():
    with open('feeds.json') as f:
        zewsfeed = json.loads(f.read())
    doc = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Feeds</title>
</head>
<body style="font-family: monospace">
</body>
</html>'''
    soup = BeautifulSoup(doc, 'lxml')
    soup.body.append(soup.new_tag('h1'))
    soup.h1.append(f"{zewsfeed['title']}. Update on {zewsfeed['date']}.")
    for feed in zewsfeed['feeds']:
        section = soup.new_tag('section')
        make_feed_section(soup, section, feed)
        soup.body.append(section)
    with open('output.html', 'w') as f:
        f.write(str(soup)+'\n')

if __name__ == '__main__':
    main()
