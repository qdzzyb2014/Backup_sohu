# -*- coding: utf-8 -*-
import os
import time
import urllib

import requests
from bs4 import BeautifulSoup

from config import BASE_DIR,BACKUP_DIR

def mkdir(backup_dir):
    dirnames = ['images', 'js', 'css']
    t = time.strftime('%Y%m%d%H%M')
    path = os.path.join(BASE_DIR, backup_dir, t)
    if os.path.exists(path):
        print u'文件夹已存在'
    else:
        for dirname in dirnames:
            os.makedirs(os.path.join(path, dirname))
    return path


def create_file(lists, get_arg, path, fe):
    lists = set(lists)
    file_index = 1
    for l in lists:
        target = l.get(get_arg)
        filepath = os.path.join(path,
                u'{fn}.{fe}'.format(fn=file_index, fe=fe))
        urllib.urlretrieve(target, filepath)
        file_index += 1


def create_inline_file(lists, path, fe):
    file_index = 1
    for l in lists:
        with open(os.path.join(path, 'inline_%d.%s'%(file_index,fe)), 'wb') as f:
            f.write(l.text)
        file_index += 1


def backup(url, backup_dir):
    print time.strftime('%Y.%m.%d %H:%M')
    path = mkdir(backup_dir)
    r = requests.get(url)
    html = r.text
    html_backup(html, path)
    soup = BeautifulSoup(html)
    images_backup(soup, path)
    css_backup(soup, path)
    js_backup(soup, path)


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


def js_backup(soup, path):
    js_list = soup.find_all('script')
    if not js_list:
        print 'There is no js.'
        return
    fe = 'js'
    path = os.path.join(path, 'js')

    ex_js_list = []
    in_js_list = []
    for js in js_list:
        if js.has_key('src'):
            ex_js_list.append(js)
        else:
            in_js_list.append(js)
    # download ex_js
    create_file(ex_js_list, 'src', path, fe)
    
    # inline
    create_inline_file(in_js_list, path, fe)
    print 'js had backuped.'


def images_backup(soup, path):
    img_list = soup.find_all('img')
    if not img_list:
        print 'There is no js'
        return
    path = os.path.join(path, 'images')
    create_file(img_list, 'src', path, 'jpg')
    print 'Iamges had backuped.'


def css_backup(soup, path):
    # ex_css
    fe = 'css'
    path = os.path.join(path, 'css')
    ex_css_list = soup.find_all('link', type='text/css')
    create_file(ex_css_list, 'href', path, 'css')

    # inline
    inline_css_list = soup.find_all('style', type='text/css')
    create_inline_file(inline_css_list, path, fe)

    print 'CSS has backuped.'


def html_backup(html, path):
    with open(os.path.join(path, 'html.html'), 'wb') as f:
        f.write(html.encode('utf-8'))
    print 'HTML has backuped.'

