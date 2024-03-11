import discord
from discord.ext import commands
from .responses import setup_bot


def init_discord_bot(token):
    bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
   
    @bot.event
    async def on_ready():
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        print(f'{bot.user} has connected to Discord successfully')


    setup_bot(bot)
    bot.run(token)


   
