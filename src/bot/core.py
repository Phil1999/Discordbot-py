import discord, os, traceback
from discord.ext import commands
from discord import app_commands
from utils.vars import GUILD_IDS 


def init_discord_bot(token):
    bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
    
    
    @bot.event
    async def setup_hook():

        dir_path = os.path.dirname(__file__)
        extensions_path = os.path.join(dir_path, "extensions")

        loaded_extensions = set()
        for filename in os.listdir(extensions_path):
            if filename.endswith(".py") and filename != "__init__.py":
                extension = f"bot.extensions.{filename[:-3]}"

                if extension not in loaded_extensions:

                    try:
                        await bot.load_extension(extension)
                        print(f"Loaded extension: {extension}")
                        loaded_extensions.add(extension)
                    except Exception as e:
                        print(f"Failed to load extension {extension}: {e}")
        

        for guild_id in GUILD_IDS:
            try:
                guild = await bot.fetch_guild(guild_id)
                # If we ever get duplicate commmands
                #bot.tree.clear_commands(guild=guild)
                await bot.tree.sync(guild=guild)
                print(f'Successfully synced commands for guild ID {guild_id}: {guild.name}')
            except Exception as e:
                print(f'Failed to sync commands for guild ID {guild_id}: {guild.name} - {e}')


    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord successfully')
   


    bot.run(token)


   
