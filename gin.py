#! /usr/bin/python3
import subprocess
from time import sleep

print('Gin is now serving Tonic.')
serveTonic = ['./tonic.py']
gitPull = ['git', 'pull']

while True:
    subprocess.run(gitPull)
    subprocess.run(serveTonic)
    sleep(10)