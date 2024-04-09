import discord
from discord.ext import commands
from .responses import setup_bot


def init_discord_bot(token):
    bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
    
    
    
    guild_ids = [1212500695719223367, 771514804895744021] # List guild IDs here

    @bot.event
    async def on_ready():
        for guild_id in guild_ids:
            try:
                await bot.tree.sync(guild=discord.Object(id=guild_id))
                print(f'Successfully synced commands for guild ID {guild_id}')
            except Exception as e:
                print(f'Failed to sync commands for guild ID {guild_id}: {e}')


    setup_bot(bot)
    bot.run(token)


   
