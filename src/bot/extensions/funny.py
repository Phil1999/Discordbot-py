import discord
from discord.ext import commands
from discord import app_commands
import os
from ..commands import funny
from utils.vars import GUILD_IDS


class FunnyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
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

       
    @app_commands.command(name='floppy', description=':susge:')
    @app_commands.guilds(*GUILD_IDS)
    async def floppy(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            file = await funny.floppy()
            await interaction.followup.send(file=file)

        except Exception as e:
            print(f"Error processing command: {e}")
            await interaction.followup.send("Failed to process command", ephemeral=True)
   
 

async def setup(bot: commands.Bot):
    await bot.add_cog(FunnyCog(bot))

