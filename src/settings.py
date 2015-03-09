import json, os, sys
from collections import OrderedDict

class Settings():
    """Program Settings"""

    # Program information
    PROGRAM_NAME = 'Curious Actors'
    PROGRAM_VER = '0.2'
    PROGRAM_AUTHOR = '@lemiffe'
    PROGRAM_WEBSITE = 'https://medium.com/@lemiffe'

    # Program arguments
    PROGRAM_ARGS = OrderedDict({
        '--verbose': 	{'name': 'verbosity', 'required': False, 'multi': False, 'msg': 'Add verbosity (for debugging purposes)'},
        '--debug': 		{'name': 'debug', 'required': False, 'multi': False, 'msg': 'Run in debug mode (avoids saving remote/local record)'},
        '--silent': 	{'name': 'silent', 'required': False, 'multi': False, 'msg': 'Run program without output'}
    })
    PROGRAM_ARGS_MIN_ONE = False # User must provide at leasto ne arg
    PROGRAM_ARGS_PRINT_NAMES = False # Print the argument 'name's in the list

    # Properties
    config = {}

    # Load configuration file
    def __init__(self):
        # Load config (JSON)
        try:
            # Change to script directory
            this_script = __file__
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(abspath)
            os.chdir(dname)
            # Load file into dictionary
            config_path = 'config.json'
            if not os.path.isfile(config_path):
                print 'Fatal error: config.json does not exist! (did you run install.sh?)'
                sys.exit(2)
            file = open(config_path, "r")
            json_str = file.read()
            self.config = json.loads(json_str.strip())
            file.close()
        except Exception as inst:
            # Die immediately as there is no config!
            print 'Fatal error: Could not load config.json - is it valid JSON?'
            sys.exit(2)
        return

    # Get a configuration variable
    def get(self, option):
        try:
            if '.' in option:
                struct = option.split('.')
                key = struct[0]
                subkey = struct[1]
                if key in self.config:
                    if subkey in self.config[key]:
                        return self.config[key][subkey]
            else:
                if option in self.config:
                    return self.config[option]
        except Exception as inst:
            print 'Fatal error: Could not read key from config.json'
            print 'Searching for ' + option
            print 'Exception: ', str(inst)
            print 'Dictionary:', self.config
            sys.exit(2)
        return None
