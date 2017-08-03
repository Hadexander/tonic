import secrets

async def tonic_token(bot):
     generatedToken = secrets.token_urlsafe(32);

     return generatedToken