from sre_compile import isstring
import discord
from discord.ext import commands
from discord import app_commands
import os
from ..commands import general
from utils.vars import GUILD_IDS, ADMIN_IDS


class GeneralCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

   
    @app_commands.command(name='help', description='Shows a list of commands')
    @app_commands.guilds(*GUILD_IDS)
    async def help(self, interaction: discord.Interaction):
        embed = general.help()
        await interaction.response.send_message(embed=embed)
      
    @app_commands.command(name='guild_gpq', description='See the total guild scores')
    @app_commands.guilds(*GUILD_IDS)
    async def total_guild_graph(self, interaction: discord.Interaction):
        try:  
            await interaction.response.defer()
            file = await general.total_score_graph()
            await interaction.followup.send(file=file)
        except Exception as e:
                command_name = interaction.data['name']
                params = {option['name']: option['value'] for option in interaction.data['options']}

                # Convert params dictionary to a string representation
                params_str = ', '.join(f'{key}={value}' for key, value in params.items()) 
                invoking_command = f"Invoked Command: {command_name}, with params - {params_str} \n" 
                
                print(invoking_command)

                traceback_str = traceback.format_exc()    
                print(traceback_str)

                error_msg = "Sorry, something went wrong." 
                await interaction.followup.send(error_msg, ephemeral=True)
    @app_commands.command(name='gpq', description="Check Culvert Scores")
    @app_commands.describe(users='List of users to query (max=4).', num_weeks='Optional: The last (num) weeks of scores')
    @app_commands.choices(num_weeks=[])
    @app_commands.guilds(*GUILD_IDS)
    async def gpq(self, interaction: discord.Interaction, users: str, num_weeks: int = None):
        try:  
            await interaction.response.defer()

            usernames_list = list(set(user.lower() for user in users.split(' ')))
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
                command_name = interaction.data['name']
                params = {option['name']: option['value'] for option in interaction.data['options']}

                # Convert params dictionary to a string representation
                params_str = ', '.join(f'{key}={value}' for key, value in params.items()) 
                invoking_command = f"Invoked Command: {command_name}, with params - {params_str} \n" 
                
                print(invoking_command)

                traceback_str = traceback.format_exc()    
                print(traceback_str)

                error_msg = "Sorry, something went wrong." 
                await interaction.followup.send(error_msg, ephemeral=True)
   

    @app_commands.command(name='converttime', description='Converts time to a Discord timestamp. see /help for more info.') 
    @app_commands.describe(timestamp="Enter a time or 'now' for the current time. Default timezone: UTC", timezone="Enter a timezone (e.g. PST or America/Los_Angeles)")
    @app_commands.guilds(*GUILD_IDS)
    async def convert_time(self, interaction: discord.Interaction, timestamp: str, timezone: str=None):
         
        try:
            await interaction.response.defer()
            result, unix_time = await general.get_discord_timestamp(timestamp, timezone)
            

            ## TODO: could refactor...
            if unix_time is None:
                await interaction.followup.send(result)
                return

            await interaction.followup.send(f"{result} - copyable timestamp: `<t:{unix_time}:F>`")

        except Exception as e:
            command_name = interaction.data['name']
            params = {option['name']: option['value'] for option in interaction.data['options']}

            # Convert params dictionary to a string representation
            params_str = ', '.join(f'{key}={value}' for key, value in params.items()) 
            invoking_command = f"Invoked Command: {command_name}, with params - {params_str} \n" 
                
            print(invoking_command)

            traceback_str = traceback.format_exc()    
            print(traceback_str)

            error_msg = "Sorry, something went wrong converting the time." 
            await interaction.followup.send(error_msg, ephemeral=True)


             
    @app_commands.command(name='cc', description="Shows the top 5 channels for culvert.")
    @app_commands.guilds(*GUILD_IDS)
    async def get_culvert_channel(self, interaction: discord.Interaction):
            try:
                await interaction.response.defer()

                result = await general.get_culvert_channel()
               
                # error occured
                if isinstance(result, str):
                    await interaction.followup.send(result)
                
                channels_string = ''
                for channel_name, latency in result:
                    channels_string += f'{channel_name} - {latency} ms\n'

                await interaction.followup.send(f'The top channels for culvert are:\n{channels_string}')
            except Exception as e:
                print(e) 
                await interaction.followup.send("Something went wrong getting channel data", ephemeral=True)
 

async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCog(bot))
    