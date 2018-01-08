#! /usr/bin/python3
import sys
from storage import db
from storage.lookups import global_settings, find_user

def help():
    print('Usage:\n\tsettings.py option <value>\nOptions:\n')
    print('\towner <id>\nRegisters discord user with <id> as a superuser for the bot.\n')
    print('\tdiscord <token>\nSets the discord API token.\n')
    print('\timgur <client_id> <client_secret> <refresh_token>\nConfigures imgur module.\n')

if(len(sys.argv) < 3):
    help()
else:
    if sys.argv[1] == 'owner':
        user = find_user(str(sys.argv[2]))
        if(user.access == 9001):
            print('id:{} already has owner-level access'.format(id))
        else:
            user.access = 9001
            user.save()
            print('Successfully granted id:{} owner-level access'.format(id))
    elif sys.argv[1] == 'discord':
        settings = global_settings()
        settings.discord_key = sys.argv[2]
        settings.save()
        print('Discord API key set.')
    elif sys.argv[1] == 'imgur':
        if(len(sys.argv) < 5):
            help()
        else:
            settings = global_settings()
            settings.imgur_id = sys.argv[2]
            settings.imgur_secret = sys.argv[3]
            settings.imgur_refresh = sys.argv[4]
            settings.save()
            print('Imgur configuration set.')
    else:
        help()
