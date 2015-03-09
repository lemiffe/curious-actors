"""
Call this like 'python install-script-gen.py'; to generate the python environment for this tool
Based on example script: https://github.com/socialplanning/fassembler/blob/master/fassembler/create-venv-script.py
"""
import os, sys
import subprocess
import re

here = os.path.dirname(os.path.abspath(__file__))
if not here.endswith("/"):
    here += "/"
base_dir = os.path.dirname(here)
script_name = os.path.join(base_dir, 'install-script.py')

try:
    import virtualenv
except ImportError, e:
    print 'Error: Virtualenv is not installed, please run the following first:'
    print 'sudo pip install virtualenv'
    sys.exit()

EXTRA_TEXT = """
import shutil, sys

def adjust_options(options, args):
    if not args:
        return # caller will raise error
    
    # We're actually going to build the venv in a subdirectory
    base_dir = args[0]
    args[0] = join(base_dir, 'venv')

def after_install(options, home_dir):
    base_dir = os.path.dirname(home_dir)

    file_content = open('dependencies.txt')
    file_content = file_content.readlines()
    dependencies = []
    for line in file_content:
        if line.strip() != '':
            dependencyListFull = [a.strip().replace(\"'\", '').replace('\"', '') for a in line.split(',')]
            dependencyList = {}
            for dependencyStr in dependencyListFull:
                dependencyList[dependencyStr.split(':')[0].strip()] = dependencyStr.split(':')[1].strip()
            dependencies.append(dependencyList)
    
    for dependency in dependencies:
        cwdDir = home_dir
        if dependency['cwd'] != 'home_dir':
            cwdDir = dependency['cwd']
        parameters = [a.strip() for a in dependency['parms'].split(' ')]
        programPath = os.path.abspath(join(home_dir, 'bin', dependency['cmd']))
        fullProgramArray = [programPath] + parameters

        call_subprocess(fullProgramArray,
                    cwd=os.path.abspath(cwdDir),
                    filter_stdout=filter_python_develop,
                    show_stdout=False)

def fs_ensure_dir(dir):
    if not os.path.exists(dir):
        logger.info('Creating directory %s' % dir)
        os.makedirs(dir)

def filter_python_develop(line):
    if not line.strip():
        return Logger.DEBUG
    for prefix in ['Searching for', 'Reading ', 'Best match: ', 'Processing ',
                   'Moving ', 'Adding ', 'running ', 'writing ', 'Creating ',
                   'creating ', 'Copying ']:
        if line.startswith(prefix):
            return Logger.DEBUG
    return Logger.NOTIFY
"""

def main():
    
    # Generate installation script
    text = virtualenv.create_bootstrap_script(EXTRA_TEXT, python_version='2.7.9')
    
    # Save script if it has been changed
    if os.path.exists(script_name):
        f = open(script_name)
        cur_text = f.read()
        f.close()
    else:
        cur_text = ''
    print 'Updating %s' % script_name
    if cur_text == 'text':
        print 'No update'
    else:
        print 'Script changed; updating...'
        f = open(script_name, 'w')
        f.write(text)
        f.close()
        print 'Filename: ' + script_name

    # Execute script (hacky, should be imported instead)
    print 'Executing installation script...'
    subprocess.call(['python', script_name, 'bin'])

    # Destroy script (will get re-created if this file runs again)
    print 'Removing installation script...'
    os.remove(script_name)

if __name__ == '__main__':
    main()