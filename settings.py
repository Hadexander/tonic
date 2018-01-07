import sys
from storage import db
from storage.lookups import store_setting

if(len(sys.argv) < 3):
    print('Usage:\n\tsettings.py option <value>\nOptions:\n')
    print('\towner\nRegisters discord user with id <value> as a superuser for the bot.\n')
    print('\tdiscord\nSets the discord API token of the bot to <value>.\n')
    print('\timgur\nSets the imgur API refresh token of the bot to <value>.\n')
else:
    if sys.argv[1] == 'owner':
        user = db.User(sha = hash(sys.argv[2]))
        db.pull(user)
        if(user.access == 9001):
            print('id:{} already has owner-level access'.format(id))
        else:
            user.access = 9001
            user.save()
            print('Successfully granted id:{} owner-level access'.format(id))
    elif sys.argv[1] == 'discord':
        store_setting('discord_api_key', sys.argv[2])
        print('Discord API key set.')
    elif sys.argv[1] == 'imgur':
        store_setting('imgur_refresh_token', sys.argv[2])
        print('Imgur refresh key set.')
