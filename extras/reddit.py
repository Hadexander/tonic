import discord
import asyncio 
import praw
from discord.ext import commands
from storage import settings

praw_creds = settings.load('PRAW')

class Reddit:
        def __init__(self):
                self.reddit = praw.Reddit(client_id= praw_creds.get('cid'), 
                                client_secret= praw_creds.get('secret'),
                                username= praw_creds.get('user'), 
                                password= praw_creds.get('pwd'), 
                                user_agent= praw_creds.get('uage'))
                self.sub_code = self.reddit.subreddit('programmerhumor+programminghorror')
                self.sub_poe = self.reddit.subreddit('pathofexile')
                self.sub_happy = self.reddit.subreddit('rarepuppers+WhatsWrongWithYourDog+eyebleach+AnimalsStuckinThings+blep')

        def query(self, subreddit):
                self.buffer = [post for post in subreddit.hot(limit=50)]
                        
"""test = Reddit()
test.query(test.sub_code)"""