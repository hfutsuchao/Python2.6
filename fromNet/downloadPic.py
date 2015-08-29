import os
import re
import requests

def get_urls(url, regex):
    urls = []
    base_url = 'http://desk.zol.com.cn'
    content = requests.get(url).content
    area = re.search(regex, content, re.S).group(0)
    tails = re.findall(r'href="(.*?)"', area)
    for tail in tails:
        urls.append(base_url + tail)
    return urls

def download_picture(url, count):
    target_dir = 'pic'
    if os.path.exists(target_dir):
        if not os.path.isdir(target_dir):
            os.remove(target_dir)
    else:
        os.mkdir(target_dir)
    content = requests.get(url).content
    picture_url = re.search(r'<img id="bigImg" src="(.*?)"', content).group(1)
    picture = requests.get(picture_url).content
    suffix = re.sub(r'.*\.', '.', picture_url)
    with open('pic/' + str(count) + suffix, 'wb') as f:
        f.write(picture)

def spider(url, count):
    regex1 = r'<ul class="pic-list2  clearfix">.*?</ul>'
    regex2 = r'<ul id="showImg".*?</ul>'
    urls = get_urls(url, regex1)
    for each_url in urls:
        picture_urls = get_urls(each_url, regex2)
        for each_picture_url in picture_urls:
            download_picture(each_picture_url, count)
            print 'Downloading picture ' + str(count)
            count += 1
    return count

def get_next_page_url(url):
    base_url = 'http://desk.zol.com.cn'
    content = requests.get(url).content
    tail = re.search(r'<a id="pageNext" href="(.*?)"', content).group(1)
    return base_url + tail

if __name__ == '__main__':
    url = 'http://desk.zol.com.cn/meinv/'
    count = 1
    count = spider(url, count)
    while True:
        key = raw_input('Input y/Y to continue download next page, or input other words to exit.')
        if re.match(r'Y', key, re.I):
            url = get_next_page_url(url)
            count = spider(url, count)
        else:
            exit()