# -*- coding: utf-8 -*-
import os
import sys
import time
import requests
import getopt
import urllib
import random
from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join('tmp', 'backup')
URL = 'http://m.sohu.com/'
TIMER = 60


def mkdir(backup_dir):
    dirnames = ['images', 'js', 'css']
    t = time.strftime('%Y%m%d%H%M')
    path = os.path.join(BASE_DIR, BACKUP_DIR, t)
    if os.path.exists(path):
        print u'文件夹已存在'
    else:
        for dirname in dirnames:
            os.makedirs(os.path.join(path, dirname))
    return path


def backup(timer=TIMER, url=URL, backup_dir=BACKUP_DIR):
    path = mkdir(backup_dir)
    r = requests.get(url)
    html = r.text
    html_backup(html, path)
    soup = BeautifulSoup(html)
    images_backup(soup, path)
    css_backup(soup, path)
    js_backup(soup, path)


def js_backup(soup, path):
    js_list = soup.find_all('script')
    if not js_list:
        print 'There is no js.'
        return
    path = os.path.join(path, 'js')
    for js in js_list:
    	filepath = os.path.join(path, u'%d.jpg' % random.randint(10, 20))
    	if js.has_key('src'):
        	link = js.get('src')
        	urllib.urlretrieve(link, filepath)
        else:
        	with open(filepath, 'wb') as f:
        		f.write(js.text.encode('utf-8'))

    print 'js had backup.'


def images_backup(soup, path):
    img_list = soup.find_all('img')
    if not img_list:
        return
    path = os.path.join(path, 'images')
    for img in img_list:
        link = img.get('src')
        alt = img.get('alt')
        filepath = os.path.join(path, u'%s.jpg' % alt)
        urllib.urlretrieve(link, filepath)
    print 'images has backup.'


def css_backup(soup, path):

    # 外部样式表
    path = os.path.join(path, 'css')
    ex_css_list = soup.find_all('link', type='text/css')
    for ex_css in ex_css_list:
        link = ex_css.get('href')
        filepath = os.path.join(path, 'home.css')
        urllib.urlretrieve(link, filepath)

    # 行内
    inline_css_list = soup.find_all('style', type='text/css')
    for inline_css in inline_css_list:
        with open(os.path.join(path, 'inline.css'), 'wb') as f:
            f.write(inline_css.text)
    print 'css has backup.'


def html_backup(html, path):
    with open(os.path.join(path, 'html.html'), 'w') as f:
        f.write(html.encode('utf-8'))
   	print 'html has backup.'


def main():
    timer = TIMER
    url = URL
    backup_dir = BACKUP_DIR
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:u:o:')
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == '-d':
            timer = int(a)
        elif o == '-u':
            url = a
        elif o == '-o':
            backup_dir = a
        else:
            assert False, 'unhandled option'

    while True:
    	print time.strftime('%Y.%m.%d %H:%M')
        backup(timer=timer, url=url, backup_dir=backup_dir)
        time.sleep(timer)


if __name__ == '__main__':
    main()
