# -*- coding: utf-8 -*-
import os
import time
import urllib
from urlparse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

from config import BASE_DIR


def mkdir(backup_dir):
    # 创建备份文件夹
    dirnames = ['images', 'js', 'css']
    t = time.strftime('%Y%m%d%H%M')
    path = os.path.join(BASE_DIR, backup_dir, t)
    if os.path.exists(path):
        print u'文件夹已存在'
    else:
        for dirname in dirnames:
            os.makedirs(os.path.join(path, dirname))
    return path


def create_external_file(lists, get_arg, path):
    # 备份外部目标文件
    lists = set(lists)
    for l in lists:
        target = l.get(get_arg)
        filename = target.split('/')[-1]
        filepath = os.path.join(path,
                        '{fn}'.format(fn=filename))
        urllib.urlretrieve(target, filepath)



def create_inline_file(lists, path, fe):
    # 备份内部目标
    lists = set(lists)
    file_index = 1
    for l in lists:
        with open(os.path.join(path,
                        'inline_%d.%s' % (file_index, fe)), 'wb') as f:
            f.write(l.text)
        file_index += 1


def backup(url, backup_dir):
    print time.strftime('%Y.%m.%d %H:%M')
    path = mkdir(backup_dir)
    r = requests.get(url)
    html = r.text
    html_backup(html, path)                     # back up html
    soup = BeautifulSoup(html, 'html.parser')
    images_backup(soup, path)                   # back up images
    css_backup(soup, path)
    js_backup(soup, path, url)                  # back up js


def js_backup(soup, path, url=None):
    js_list = soup.find_all('script')
    if not js_list:
        print 'There is no js.'
        return
    fe = 'js'
    path = os.path.join(path, 'js')

    ex_js_list , in_js_list = [], []
    for js in js_list:
        if js.has_attr('src'):
            if not is_abs_url(js.get('src')):
                js['src'] = urljoin(url, js.get('src'))
            ex_js_list.append(js)
        else:
            in_js_list.append(js)
    # download ex_js
    create_external_file(ex_js_list, 'src', path)

    # inline
    create_inline_file(in_js_list, path, fe)
    print 'js had backuped.'


def images_backup(soup, path):
    img_list = soup.find_all('img')
    if not img_list:
        print 'There is no js'
        return
    path = os.path.join(path, 'images')
    create_external_file(img_list, 'src', path)
    print 'Iamges had backuped.'


def css_backup(soup, path):
    # ex_css
    fe = 'css'
    path = os.path.join(path, 'css')
    ex_css_list = soup.find_all('link', type='text/css')
    create_external_file(ex_css_list, 'href', path)

    # inline
    inline_css_list = soup.find_all('style', type='text/css')
    create_inline_file(inline_css_list, path, fe)
    print 'CSS has backuped.'


def html_backup(html, path):
    with open(os.path.join(path, 'html.html'), 'wb') as f:
        f.write(html.encode('utf-8'))
    print 'HTML has backuped.'


def is_abs_url(url):
    r = urlparse(url)
    return r.scheme
