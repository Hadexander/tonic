import subprocess
import os
from time import sleep

print('Testing aliases...')
python = None
py_aliases = ['python3', 'python']
for alias in py_aliases:
    so = subprocess.getstatusoutput(alias+' -V')
    if so[0] == 0:
        python = alias
        print('{} found.'.format(alias))
        break

if not python:
    print('Could not find a valid python alias.')
    exit(0)

print('Gin is now serving Tonic.')
cmd = [python, 'tonic.py']
gitcmd = ['git', 'pull']

def gitPull():  
    print('Pulling from git')
    subprocess.run(gitcmd)

def serveTonic():
    return subprocess.run(cmd)

exitCode = -1
while(exitCode != 0):
    result = serveTonic()
    exitCode = result.returncode
    print('Tonic exited with code {}'.format(exitCode))
    sleep(5)
    if exitCode == 420:
        gitPull()
