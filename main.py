# -*- coding: utf-8 -*-
import sys
import time
import getopt
from multiprocessing import Process
from backup import backup
from config import TIMER, URL, BACKUP_DIR


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
		p = Process(target=backup, args=(url, backup_dir))
		p.start()
		time.sleep(timer)


if __name__ == '__main__':
	main()
