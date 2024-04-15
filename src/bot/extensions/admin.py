import discord
from discord.ext import commands
from discord import app_commands
import os
from ..commands import admin
from utils.vars import GUILD_IDS, ADMIN_IDS
from utils.decorators import is_admin


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='update_database', description='Reads in a csv file which is added to the main database (ADMIN)')  
    @app_commands.describe(attachment= "Enter a csv file.")
    @app_commands.guilds(*GUILD_IDS)
    @is_admin()
    async def read_csv_data(self, interaction: discord.Interaction, attachment: discord.Attachment):
        try:
            await interaction.response.defer()            
            response = await admin.update_db(attachment)
            await interaction.followup.send(response)
        except Exception as e:
            print(f"Error processing command: {e}")
            await interaction.followup.send("Failed to process command.", ephemeral=True)


    @app_commands.command(name='database_to_local', description='Updates local data (ADMIN)')
    @app_commands.guilds(*GUILD_IDS)
    @is_admin()
    async def database_to_local(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()            
            response = await admin.db_to_local()
            await interaction.followup.send(response)
        except Exception as e:
            print(f"Error processing command: {e}")
            await interaction.followup.send("Failed to process command.", ephemeral=True)

 
   
 

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))
