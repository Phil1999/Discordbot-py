import discord
import responses


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def init_discord_bot(token):
    TOKEN = token
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is running properly.')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content).strip()
        channel = str(message.channel)

        print(f"{username} said '{user_message}' ({channel})")

        # If the message is supposed to be private
        if user_message and user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)


    client.run(TOKEN)
