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
serveTonic = [python, 'tonic.py']
gitPull = ['git', 'pull']

while True:
    subprocess.run(gitPull)
    subprocess.run(serveTonic)
    sleep(5)