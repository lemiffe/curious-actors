# Standard libraries
import sys, traceback, re, os, shutil
from collections import defaultdict
from decimal import *
from datetime import datetime, date, time
from collections import OrderedDict
import json
import random

# Custom libraries and wrappers
from lib.docproc import *
from lib.debug import *
from lib.dates import *
from lib.strings import *
from lib.mongo import *
from lib.arguments import *

# Application modules
from settings import *

# Main class (contains application code)
class App():

	# General properties
	
	settings = None
	debug = None
	args = []

	# Constructor

	def __init__(self, args, settings=None, debug=None):
		self.args = args
		self.settings = settings
		self.debug = debug
		return

	# Helper methods

	def shout(self, text):
		self.debug.Output(text, 0)

	def say(self, text):
		self.debug.Output(text, 1)

	def say_inline(self, text):
		self.debug.OutputInline(text, 1)

	def whisper(self, text):
		self.debug.Output(text, 2)

	def whisper_inline(self, text):
		self.debug.OutputInline(text, 2)

	def display_exec_time(self, start_time, end_time):
		self.debug.NewLine(1)
		exec_time = self.time_diff(start_time, end_time)
		exec_time_str = ("%s seconds" % exec_time)
		self.say('Program has terminated!')
		self.say('Execution time: ' + exec_time_str)

	def time_diff(self, start, end):
		'''Time difference in seconds'''
		return datetime.combine(date.today(), end) - datetime.combine(date.today(), start)

	def run(self):

		# Initialise program
		self.debug.Title(self.settings.PROGRAM_NAME, self.settings.PROGRAM_VER, self.settings.PROGRAM_AUTHOR, self.settings.PROGRAM_WEBSITE, 1)
		args = self.args
		exit_code = 0

		# Start timer
		start_time = datetime.now().time()

		try:
			
			# This is where the main loop will go
			# <start>
			self.say('start')
			self.say('end')
			# <end>

		except KeyboardInterrupt as ex:
			self.say('Manually stopped!')
			exit_code = 0 # Exit with 0 (graceful exit)

		except Exception as ex:
			self.say('Error: ' + ex.__str__())
			if ArgLib.GetDebugLevel(args) == 2:
				traceback.print_exc(file=sys.stdout)
			exit_code = 2 # Exit with 2 (exception)
		
		# Display execution time and exit
		end_time = datetime.now().time()
		self.display_exec_time(start_time, end_time)

		# Return exit code
		return exit_code

# Execute program!
if __name__ == '__main__':
	
	# Load arguments
	args = ArgLib.LoadDynamicArgs(sys.argv[1:])
	
	# Set variables + directories
	debug_level = ArgLib.GetDebugLevel(args)
	script_name = os.path.realpath(__file__).split('/')[-1]
	DocProc.ChangeDirectory(__file__)
	
	# Set up libs
	settings = Settings()
	debug = Debug(debug_level, DocProc.LineEnd())
	
	# Check arguments are correct (or list arguments)
	if not ArgLib.ValidateArgs(args, script_name, settings.PROGRAM_ARGS, settings.PROGRAM_ARGS_MIN_ONE, settings.PROGRAM_ARGS_PRINT_NAMES):
		sys.exit(0) # exit gracefully
	
	# Initiate application
	app = App(args, settings, debug)
	exit_code = app.run()

	sys.exit(exit_code)
