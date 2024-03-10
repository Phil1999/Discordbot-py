from .commands import general
import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from utils.decorators import delete_invoke_message

def setup_bot(bot):
    guild_id = 1212500695719223367

    @bot.tree.command(name='help', description='help command')
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(general.help())
      
       
    @bot.tree.command(name="gpq", description="Testing", guild=discord.Object(id=guild_id))
    @app_commands.describe(usernames='list of usernames to query (max=4).')
    async def gpq(interaction: discord.Interaction, usernames: str):
        try:  
            await interaction.response.defer()

            async def command_logic():
                usernames_list = usernames.split(' ')
                return await general.send_character_image_url(usernames_list)

            result, file = await asyncio.wait_for(command_logic(), timeout=15)

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
        except asyncio.TimeoutError:
            # Handle the case where the command_logic takes too long.
            await interaction.followup.send("Sorry, the command took too long to process.")
