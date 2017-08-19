import subprocess
import os
from time import sleep

print('Gin is now serving Tonic.')
cmd = 'python tonic.py'
gitcmd='git pull'

def gitPull():  
    print('Pulling from git')
    subprocess.run(gitcmd, shell=True)

def serveTonic():
    return subprocess.run(cmd, shell=True)

exitCode = -1
while(exitCode != 0):
    result = serveTonic()
    exitCode = result.returncode
    print('Tonic exited with code {}'.format(exitCode))
    print(result.stdout)
    sleep(5)
    if exitCode == 420:
        gitPull()
