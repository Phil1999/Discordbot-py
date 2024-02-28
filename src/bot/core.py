import discord
from . import responses

client = discord.Client(intents=discord.Intents.all())

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready():
    print(f'{client.user} is running properly.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    user_message = str(message.content).strip()
    is_private = user_message.startswith('?')
    if is_private:
        user_message = user_message[1:]
    
    await send_message(message, user_message, is_private)

def init_discord_bot(token):
    client.run(token)