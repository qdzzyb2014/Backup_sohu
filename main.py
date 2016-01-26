# -*- coding: utf-8 -*-
import sys
import os
import time
import getopt
from multiprocessing import Process

import requests
from bs4 import BeautifulSoup

import backup
from config import BASE_DIR, TIMER, URL, BACKUP_DIR, DIRNAMES


def mkdir(backup_dir):
    # 创建备份文件夹
    t = time.strftime('%Y%m%d%H%M')
    path = os.path.join(BASE_DIR, backup_dir, t)
    if os.path.exists(path):
        print 'doc has existed'
    else:
        for dirname in DIRNAMES:
            if dirname != 'html':
                os.makedirs(os.path.join(path, dirname))
    return path


def back_up(url, backup_dir):
    print time.strftime('%Y.%m.%d %H:%M')
    path = mkdir(backup_dir)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for dirname in DIRNAMES:
        getattr(backup, '{dn}_backup'.format(dn=dirname))(
            soup, path)


def main():
    timer = TIMER
    url = URL
    backup_dir = BACKUP_DIR
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:u:o:')
    except getopt.GetoptError as err:
        print str(err)
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
            # create setprocess
        p = Process(target=back_up, args=(url, backup_dir))
        p.start()
        time.sleep(timer)


if __name__ == '__main__':
    main()
