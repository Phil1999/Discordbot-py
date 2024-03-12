from .commands import general
import discord, traceback
from discord.ext import commands
from discord import app_commands
from utils.decorators import delete_invoke_message

def setup_bot(bot):
    
    guild_ids = [1212500695719223367, 771514804895744021]
    guilds = [discord.Object(id=guild_id) for guild_id in guild_ids]
    
    @bot.tree.command(name='floppy', description=':susge:', guilds=guilds)
    async def floppy(interaction: discord.Interaction):
        await interaction.response.defer()

        file = await general.floppy()
        await interaction.followup.send(file=file)

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
                await interaction.followup.send(error_msg)
   

    @bot.tree.command(name='converttime', description='Converts time to a Discord timestamp. See /help for more info.', guilds=guilds)
    @app_commands.describe(timestamp="Enter a time or 'now' for the current time. Default timezone: UTC", timezone="Enter a timezone (e.g. PST or America/Los_Angeles)")
    async def convert_time(interaction: discord.Interaction, timestamp: str, timezone: str=None):
         
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
            await interaction.followup.send(error_msg)




