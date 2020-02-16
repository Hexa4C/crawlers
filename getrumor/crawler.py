#coding:utf-8
import time
import codecs
import requests
import json
import re
from bs4 import BeautifulSoup


def get_homepage():
    # get articles ids in home page
    r = requests.get('https://vp.fact.qq.com/home')
    text = r.text
    r.close()
    soup = BeautifulSoup(text, "html.parser")
    items = soup.find_all('li')
    ids = [li.attrs['id'] for li in items]
    return ids


def get_loaded():
    # load more articles
    ids = []
    i = 1
    while(True):
        url = 'http://vp.fact.qq.com/loadmore?artnum=%d&page=%d&_=%d&callback=%s' % (0, i, int(time.time() * 1000), 'jsonp')
        r = requests.get(url)
        back_value = r.text
        r.close()
        items = json.loads(back_value[6:-1])
        if len(items['content']) == 0:
            break
        content_ids = [item['id'] for item in items['content']]
        ids += content_ids
        i += 1
        time.sleep(0.1)
        print("finished page ", i, "!")
    return ids


def get_article(id):
    url = 'https://vp.fact.qq.com/article?id=%s' % id
    r = requests.get(url)
    article = r.text
    soup = BeautifulSoup(article, "html.parser")
    # title
    title = soup.find('h1').text
    # subtitle
    pattern = re.compile(r"const originRumor = `(.|\n)*`;")
    script = soup.find('script', {'type':'text/javascript'}, text=pattern)
    subtitle = pattern.search(script.text).group(0)[22:-2]
    # label
    try:
        mark = soup.find('span', {'class': 'mark_title doubt_mark'})
        if mark == None:
            mark = soup.find('span', {'class': 'mark_title fake_mark'})
        if mark == None:
            mark = soup.find('span', {'class': 'mark_title true_mark'})
        label = mark.text
    except:
        label = ""
        print(url)
    # point
    try:
        point = soup.find('div', {'class': 'check_content_points'}).text
    except:
        point = ""
        print(url)
    # source
    try:
        source_div = soup.find('div', {'class': 'check_content_text check_content_writer'})
        source_text = source_div.text
        institute = source_div.find('span').text
        source = source_text[: source_text.find(institute)] + " " + institute
    except:
        source = ""
        print(url)
    return {
        'title': title,
        'subtitle': subtitle,
        'label': label,
        'point': point,
        'source': source
    }


def main():
    ids = get_homepage()
    ids += get_loaded()
    articles = []
    for id in ids:
        info = get_article(id)
        articles.append(info)
        time.sleep(0.1)
    # make json file readable
    print_json = json.dumps(articles, indent=4, ensure_ascii=False)
    with codecs.open('articles.json', 'w', 'utf8') as f:
        f.write(print_json)

if __name__ == "__main__":
    main()