import subprocess
import os

print('Gin is now serving Tonic.')
os.chdir('C:/Users/MT/tonic')

def gitPull():
    subprocess.run('git pull')
    serveTonic()

cmd = 'python tonic.py'
def serveTonic():
    run = subprocess.run(cmd)
    exitCode = serveTonic().returncode
    if exitCode == 1:
        gitPull()

serveTonic()