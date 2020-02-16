import requests
import os
import time
from bs4 import BeautifulSoup


def get_books(url, path):
    r = requests.get(url)
    text = r.text
    charset = r.encoding
    r.close()
    text = text.encode(charset).decode('utf8')
    soup = BeautifulSoup(text, "html.parser")
    items = soup.find_all('li', {'class':'fl js_cp'})
    for item in items:
        links = item.find_all('a')
        title = links[1].text + '.pdf'
        print("Get ", title, "...")
        li = url + links[3]['href'][2:]
        book_req = requests.get(li)
        with open(path + title, 'wb') as f:
            f.write(book_req.content)
        book_req.close()
        time.sleep(0.1)


def get_pagelinks():
    url = "http://bp.pep.com.cn/jc/"
    r = requests.get(url)
    text = r.text
    charset = r.encoding
    r.close()
    text = text.encode(charset).decode('utf8')
    soup = BeautifulSoup(text, "html.parser")
    items = soup.find_all('div', {'class': 'list_sjzl_jcdzs2020'})
    pages = {}
    for item in items:
        maintitle = item.find('h5').text
        subpages = {}
        for a in item.find_all('a'):
            title = a.text
            l = url + a['href'][2:]
            subpages[title] = l
        pages[maintitle] = subpages
    return pages


def main():
    store_path = "../../../../media/books/textbooks/"
    print("Get all page links......")
    pages = get_pagelinks()
    time.sleep(0.1)
    #dirset = ["普通高中课程标准实验教科书"]
    #bookset = ["数学教科书", "物理教科书", "俄语教科书", "俄语教师教学用书"]
    for (subpath, links) in pages.items():
        #if subpath not in dirset:
        #    continue
        print("Get ", subpath, "...")
        for (subsubpath, link) in links.items():
            #if subsubpath not in bookset:
            #    continue
            print("Get ", subsubpath, "...")
            path = store_path + subpath + "/" + subsubpath + "/"
            os.makedirs(path)
            get_books(link, path)


if __name__ == "__main__":
    main()