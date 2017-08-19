import subprocess
import os

print('Gin is now serving Tonic.')
os.chdir('C:/Users/MT/tonic')

cmd = 'python tonic.py'
def serveTonic():
    run = subprocess.run(cmd)
    return run

def gitPull():
    subprocess.run('git pull')

exitCode = serveTonic().returncode
if exitCode == 1:
    print('Tonic upgrade function called.')
    print('Updating git repo...')
    gitPull()
    print('Git pull complete. Serving new Tonic.')
    serveTonic()