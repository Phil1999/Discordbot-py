import discord
from utils.scraper import get_character_details
from utils.plot import *


embed_side_color = discord.Color.blue() 

def help():
    embed = discord.Embed()
    embed.color = embed_side_color 
    embed.title = "*Commands*"
    embed.set_footer(text= "Schulich Bot")
    embed.add_field(name="Schulich Help", value="\n`/help` \n" +
                                 "Shows this message.\n\n", inline=False)
    embed.add_field(
    name="Culvert",
    value=(
        "\n`/gpq [names], optional 'num_weeks (num)'` \n"
        "Enter a **single** username to receive an image of their Culvert score.\n"
        "For **2-4** usernames, you will receive a comparative graph image against all listed players.\n"
        "Enter the optional param `num_weeks` to show the last **'num'** weeks of culvert scores. \n\n"
        "*Note: A maximum of **4** usernames can be entered.*\n\n"
        ),
    inline=False)

    return embed;


async def send_character_image_url(usernames):
    
    NUM_USERS = len(usernames)

    MAX_USERS = 4
    MIN_USERS = 1

    valid_params = usernames and MIN_USERS <= len(usernames) <= MAX_USERS
    
    if not valid_params:
        return f"Please provide at least {MIN_USERS} username and up to {MAX_USERS} maximum. Usage: `!gpq <username> ...`", None
    
    comparison(get_data(), usernames)
    file = discord.File(f'assets/images/graph.png', filename = 'graph.png')

    if NUM_USERS == 1:
        character_details = get_character_details(usernames[0])
        if character_details['found'] is not True:
            return "The user you entered couldn't be found", None

        print(character_details)
        embed = discord.Embed()
        embed.color = embed_side_color
        title = f"{character_details['name']}"
        embed.title = title
        embed.set_thumbnail(url=character_details['image_url'])

        stat_dict = stats(get_data(), usernames[0])

        des = f"Level {character_details['level'] + ' ' +  character_details['class']}"
        embed.description = des
        embed.set_footer(text='Rank #' + str(stat_dict['rank']) + ' of ' + str(stat_dict['numptcp']) + ' in most recent week')
        embed.add_field(name='Participation (%)', value = stat_dict['ptcp'], inline = False)
        embed.add_field(name='Min', value = stat_dict['min'], inline = True)
        embed.add_field(name='Average', value = stat_dict['mean'], inline = True)
        embed.add_field(name='Max', value = stat_dict['max'], inline = True)
        embed.set_image(url = 'attachment://graph.png')
        return embed, file
    else:
        return None, file
    
   
