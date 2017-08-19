import subprocess
import os

print('Gin is now serving Tonic.')
cmd = 'python tonic.py'
gitcmd = 'git pull'

def gitPull():
    print('Pulling from git')
    subprocess.run(gitcmd)

def serveTonic():
    run = subprocess.run(cmd)
    exitCode = run.returncode
    if exitCode == 420:
        print('Client close detected')
        print(exitCode)
        gitPull()
        serveTonic()

serveTonic()