import discord, os
from discord.ext import commands
from .responses import setup_bot


EXTENSIONS = ("bot.extensions.general",)

def init_discord_bot(token):
    bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
    
    
    @bot.event
    async def setup_hook():
        for extension in EXTENSIONS:
            await bot.load_extension(extension)

        guild_ids = [1212500695719223367, 771514804895744021] # List guild IDs here
        for guild_id in guild_ids:
            try:
                guild = await bot.fetch_guild(guild_id)
                await bot.tree.sync(guild=discord.Object(id=guild_id))
                print(f'Successfully synced commands for guild ID {guild_id}: {guild.name}')
            except Exception as e:
                print(f'Failed to sync commands for guild ID {guild_id}: {guild.name} - {e}')

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord successfully')
    
    @bot.event
    async def on_message(message):
        
        if message.author.id == 172520567163977729:
            if 'nerd' in message.content.lower():
                await message.channel.send(message.content + ' :nerd: :point_up:')
            elif 'osmow' in message.content.lower():
                await message.channel.send("osmows mid" + " :yawning_face:")
        elif message.author.id == 108311639958265856:
            if all(x in message.content.lower() for x in ['hold', 'nuts']) or \
                all(x in message.content.lower() for x in ['hold', 'nut']):
                await message.channel.send(message.content + ' :nerd: :point_up:')
        elif message.author.id == 467243435380965397:
            if 'nono' in message.content.lower():
                await message.channel.send("yes yes, stop lying")
        elif message.author.id == 120696277104066564:
            if 'my fault' in message.content.lower():
                await message.channel.send("yea ur fault")


    #setup_bot(bot)
    #bot.setup_hook = setup_hook
    bot.run(token)


   
