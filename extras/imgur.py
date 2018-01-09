from datetime import datetime, timedelta
import asyncio
import aiohttp
from storage.lookups import global_settings

async def _update_access_token(settings):
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
    settings = global_settings()
    await _update_access_token(settings)
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization':'Client-ID '+settings.imgur_id,
            'Authorization':'Bearer '+settings.imgur_access
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
    settings = global_settings()
    await _update_access_token(settings)
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization':'Bearer '+settings.imgur_access
        }
        await session.delete('https://api.imgur.com/3/image/'+id, headers=headers)
