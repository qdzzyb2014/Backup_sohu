# -*- coding: utf-8 -*-
import os
import time
import urllib
import random

import requests
from bs4 import BeautifulSoup

from config import TIMER, URL, BACKUP_DIR, BASE_DIR, BACKUP_TYPE


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


def backup(url=URL, backup_dir=BACKUP_DIR):
    print time.strftime('%Y.%m.%d %H:%M')
    path = mkdir(backup_dir)
    r = requests.get(url)
    html = r.text
    html_backup(html, path)
    soup = BeautifulSoup(html)
    '''
    images_backup(soup, path)
    js_backup(soup, path)
    '''
    for backup_type in BACKUP_TYPE.keys():
        if backup_type == 'img':
            download_path = os.path.join(path, 'images')
        else:
            download_path = os.path.join(path, BACKUP_TYPE[backup_type])

        download(soup, download_path, backup_type)

    css_backup(soup, path)
    print ''


def download(soup, path, backup_type):
    result_list = set(soup.find_all(backup_type))
    if not result_list:
        print 'There is no {type}'.format(type=backup_type)
        return

    filename = 1
    for res in result_list:
        link = res.get('src')
        filepath = os.path.join(path,
                u'{fn}.{fe}'.format(fn=filename, fe=BACKUP_TYPE[backup_type]))
        urllib.urlretrieve(link, filepath)
        filename += 1



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

'''
def js_backup(soup, path):
    js_list = soup.find_all('script')
    if not js_list:
        print 'There is no js.'
        return
    path = os.path.join(path, 'js')
    for js in js_list:
        link = js.get('src')
        filepath = os.path.join(path, u'%d.js' % random.randint(10, 20))
        urllib.urlretrieve(link, filepath)
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

'''


def html_backup(html, path):
    with open(os.path.join(path, 'html.html'), 'wb') as f:
        f.write(html.encode('utf-8'))
        print 'html has backup.'
