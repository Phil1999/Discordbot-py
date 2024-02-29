import discord
from . import responses

client = discord.Client(intents=discord.Intents.all())

async def send_message(message, is_private):
    try:
        response = await responses.handle_response(message)

        if isinstance(response, str):
            # It's a simple string message
            target = message.author if is_private else message.channel
            await target.send(response)
        elif isinstance(response, discord.Embed):
            # It's an embed, likely from send_image_url
            await message.channel.send(embed=response)
    except Exception as e:
        print(e)

@client.event
async def on_ready():
    print(f'{client.user} is running properly.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    

    if message.content.startswith('!'):
        is_private=False
        await send_message(message, is_private=is_private)

    elif message.content.startswith('?'):
        is_private=True
        await send_message(message, is_private=is_private)

def init_discord_bot(token):
    client.run(token)