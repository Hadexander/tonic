import subprocess
import os

print('Gin is now serving Tonic.')
cmd = ['python',  'tonic.py']
gitcmd=['git', 'pull']

def gitPull():  
    print('Pulling from git')
    subprocess.run(gitcmd)

def serveTonic():
    return subprocess.run(cmd).returncode

exitCode = -1
while(exitCode != 0):
    exitCode = serveTonic()
    print('Tonic exited with code {}'.format(exitCode))
    if exitCode == 420:
        gitPull()
