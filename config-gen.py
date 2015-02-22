import sys, traceback, re, os, shutil
from collections import defaultdict
from decimal import *
from datetime import datetime, date, time
from collections import OrderedDict
import json
import random

def get_base_config():
	return json.dumps({
		'mongo': {
			'host': 'localhost',
			'port': 27017,
			'db': 'curious',
			'collection_bots': 'actors'
		}
	})

def main():
	# Change to script directory
	this_script = __file__
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname)
	# Write base configuration to file
	try:
		config_path = 'src/config.json'
		if not os.path.isfile(config_path):
			file = open(config_path, "w")
			file.write(get_base_config())
			file.close()
			exit(0)
		else:
			print 'Config already exists!'
			exit(1)
	except Exception as inst:
		print 'Could not generate configuration file!'
		print str(inst)
		exit(2)

# Execute program
if __name__ == '__main__':
	main()
