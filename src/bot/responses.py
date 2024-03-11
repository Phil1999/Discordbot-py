from .commands import general
import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from utils.decorators import delete_invoke_message

def setup_bot(bot):
    
    guild_ids = [1212500695719223367, 771514804895744021]

    guilds = [discord.Object(id=guild_id) for guild_id in guild_ids]

    @bot.tree.command(name='help', description='Shows a list of commands', guilds=guilds)
    async def hello(interaction: discord.Interaction):
        embed = general.help()
        await interaction.response.send_message(embed=embed)
      
       
    @bot.tree.command(name="gpq", description="Check culvert scores", guilds=guilds)
    @app_commands.describe(users='List of users to query (max=4).', num_weeks='Optional: The last (num) weeks of scores')
    @app_commands.choices(num_weeks=[])
    async def gpq(interaction: discord.Interaction, users: str, num_weeks: int = None):
        try:  
            await interaction.response.defer()

            usernames_list = list(set(users.split(' ')))
            result, file = await general.send_character_image_url(usernames_list, num_weeks)

            
            # Now, respond using follow-up for all scenarios.
            if isinstance(result, str):
                # If the result is a simple message.
                await interaction.followup.send(result)
            elif result is None and file is not None:
                # If there's only a file to send.
                await interaction.followup.send(file=file)
            elif isinstance(result, discord.Embed):
                # If there's an embed, optionally with a file.
                if file is not None:
                    await interaction.followup.send(file=file, embed=result)
                else:
                    await interaction.followup.send(embed=result)
        except Exception as e:
                print(e)
                await interaction.followup.send("Sorry, something went wrong.")
