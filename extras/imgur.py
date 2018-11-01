from datetime import datetime, timedelta
import asyncio
import aiohttp
from storage import settings

async def _update_access_token(settings):
    """Generates or updates an imgur API access token using imgur account data provided in settings."""
    now = datetime.now()
    if(settings.imgur_expiration < now):
        async with aiohttp.ClientSession() as session:
            body = {
                'refresh_token':settings.imgur_refresh,
                'client_id':settings.imgur_id,
                'client_secret':settings.imgur_secret,
                'grant_type':'refresh_token'
            }
            async with session.post('https://api.imgur.com/oauth2/token', data=body) as response:
                if(response.status == 200):
                    resp = await response.json()
                    settings.imgur_access = resp.get('access_token')
                    exp = resp.get('expires_in', 0)
                    settings.imgur_expiration = now + timedelta(seconds=exp)
                    settings.save()

async def image_upload(url):
    """Uploads an image to imgur by url. Returns a link and image id on success, error message on failure."""
    config = settings.load('Imgur')
    #disabled temporarily
    #await _update_access_token(settings)
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization':'Client-ID '+config.get('id'),
            'Authorization':'Bearer '+config.get('access')
        }
        body = {
            'image':url
        }
        async with session.post('https://api.imgur.com/3/image', headers=headers, data=body) as response:
            resp = await response.json()
            if(resp['status'] == 200):
                return {'link':resp['data']['link'], 'id':resp['data']['id']}
            else:
                return {'error':resp['data']['error']['message']}


async def image_delete(id):
    """Deletes an image from imgur."""
    config = settings.load('Imgur')
    #await _update_access_token(settings)
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization':'Bearer '+config.get('access')
        }
        await session.delete('https://api.imgur.com/3/image/'+id, headers=headers)
