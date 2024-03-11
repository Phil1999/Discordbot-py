import discord
from discord.ext import commands
from .responses import setup_bot


def init_discord_bot(token):
    bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
    guild_id = 771514804895744021 
    @bot.event
    async def on_ready():
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync(guild=discord.Object(id=guild_id))
        print(f'{bot.user} has connected to Discord successfully')


    setup_bot(bot)
    bot.run(token)


   
