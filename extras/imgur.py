from datetime import datetime, timedelta
import asyncio
import aiohttp
from storage import settings

time_format = "%Y-%m-%dT%H:%M:%S"

async def _update_access_token(config):
    """Generates or updates an imgur API access token using imgur account data provided in config."""
    now = datetime.now()
    exp_str = config.get('expiration')
    try:
        exp = datetime.strptime(str(exp_str), time_format)
    except ValueError:
        exp = None
    if not exp or exp < now:
        async with aiohttp.ClientSession() as session:
            body = {
                'refresh_token':config.get('refresh'),
                'client_id':config.get('id'),
                'client_secret':config.get('secret'),
                'grant_type':'refresh_token'
            }
            async with session.post('https://api.imgur.com/oauth2/token', data=body) as response:
                if(response.status == 200):
                    resp = await response.json()
                    config['access'] = resp.get('access_token')
                    exp_seconds = resp.get('expires_in', 0)
                    exp = now + timedelta(seconds=exp_seconds)
                    config['expiration'] = datetime.strftime(exp, time_format)
                    settings.save('Imgur', config)

async def image_upload(url):
    """Uploads an image to imgur by url. Returns a link and image id on success, error message on failure."""
    config = settings.load('Imgur')
    await _update_access_token(config)
    async with aiohttp.ClientSession() as session:
        headers = {
            #'Authorization':'Client-ID '+config.get('id'),
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
    await _update_access_token(config)
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization':'Bearer '+config.get('access')
        }
        await session.delete('https://api.imgur.com/3/image/'+id, headers=headers)
