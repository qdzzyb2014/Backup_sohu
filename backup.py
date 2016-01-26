# -*- coding: utf-8 -*-
import os
import urllib
from urlparse import urlparse, urljoin


def create_external_file(t_tag, get_arg, path):
    # 备份外部目标文件
    target = t_tag.get(get_arg)
    filename = target.split('/')[-1]
    filepath = os.path.join(path,
                            '{fn}'.format(fn=filename))
    if not os.path.exists(filepath):
        urllib.urlretrieve(target, filepath)


def create_inline_file(t_tag, path, fe, f_index):
    # 备份内部目标
    with open(os.path.join(path,
                           'inline_%d.%s' % (f_index, fe)), 'wb') as f:
        f.write(t_tag.text)


def js_backup(soup, path, url=None):
    js_list = soup.find_all('script')
    if not js_list:
        print 'There is no js.'
        return
    fe = 'js'
    path = os.path.join(path, 'js')

    inline_file_index = 0  # for inline file name
    for js in js_list:
        if js.has_attr('src'):
            # check the url
            if not is_abs_url(js.get('src')):
                js['src'] = urljoin(url, js.get('src'))
            # download ex_js
            create_external_file(js, 'src', path)
        else:
            # download inline
            create_inline_file(js, path, fe, inline_file_index)
            inline_file_index += 1

    print 'js had backed up.'


def images_backup(soup, path):
    img_list = soup.find_all('img')
    if not img_list:
        print 'There is no images.'
        return
    path = os.path.join(path, 'images')
    for img in img_list:
        create_external_file(img, 'src', path)
    print 'Iamges had backed up.'


def css_backup(soup, path):
    # ex_css
    fe = 'css'
    path = os.path.join(path, 'css')
    ex_css_list = soup.find_all('link', type='text/css')
    if ex_css_list:
        for ex_css in ex_css_list:
            create_external_file(ex_css, 'href', path)

    # inline
    inline_css_list = soup.find_all('style', type='text/css')
    if inline_css_list:
        inline_file_index = 0
        for css in inline_css_list:
            create_inline_file(css, path, fe, inline_file_index)
            inline_file_index += 1
    print 'CSS has backed up.'


def html_backup(soup, path):
    with open(os.path.join(path, 'index.html'), 'wb') as f:
        f.write(soup.prettify().encode('utf-8'))
    print 'HTML has backed up.'


def is_abs_url(url):
    r = urlparse(url)
    return r.scheme
