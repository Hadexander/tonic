import sys
import shelve

print('Usage:\n\taddowner.py <id>\n')
print('Registers discord user <id> as a superuser for the bot.')

with shelve.open('storage') as db:
    owners = db.get('owners', [])
    if(len(sys.argv) > 1):
        id = sys.argv[1]
        if id not in owners:
            print('Added '+id)
            owners.append(id)
            db['owners'] = owners
    print("Current owners:\n"+repr(owners))