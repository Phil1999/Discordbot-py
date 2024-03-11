import discord
from utils.scraper import get_character_details
from utils.plot import *
from datetime import datetime, timezone

embed_side_color = discord.Color.blue() 

def help():
    embed = discord.Embed()
    embed.color = embed_side_color 
    embed.title = "*Commands*"
    embed.set_footer(text= "Schulich Bot")
    
    embed.add_field(
        name="Schulich Help",
        value="\n`/help` \n" + "Shows this message.\n\n", 
        inline=False
    )


    embed.add_field(
        name="Culvert",
        value=(
            "\n`/gpq [names], optional 'num_weeks (num)'` \n"
            "Enter a **single** username to receive an image of their Culvert score.\n"
            "For **2-4** usernames, you will receive a comparative graph image against all listed players.\n"
            "Enter the optional param `num_weeks` to show the last **'num'** weeks of culvert scores. \n\n"
            "*Note: A maximum of **4** usernames can be entered.*\n\n"
        ),
        inline=False
    )

    embed.add_field(
        name="Discord Timestamp",
        value=(
            "\n`/converttime (timestamp), or 'now' for the current time` \n"
            "Enter a timestamp in UTC time to convert it into a Discord timestamp. \n"
        ),
        inline=False
    )

    return embed;


async def send_character_image_url(usernames, num_weeks):
    
    NUM_USERS = len(usernames)

    MAX_USERS = 4
    MIN_USERS = 1

    valid_params = usernames and MIN_USERS <= len(usernames) <= MAX_USERS
    
    if not valid_params:
        return f"Please provide at least {MIN_USERS} username and up to {MAX_USERS} maximum. Usage: `!gpq <username> ...`", None
    
    if num_weeks is not None:
        if type(num_weeks) != int or num_weeks < 1:
            return "Number of weeks must be a postive integer", None
        else:
            comparison(get_data(), usernames, num_weeks)
    else:
        comparison(get_data(), usernames, None)
    file = discord.File(f'assets/images/graph.png', filename = 'graph.png')

    if NUM_USERS == 1:
        character_details = get_character_details(usernames[0])
        if character_details['found'] is not True:
            return "The user you entered couldn't be found", None
        
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

# Note that we expect to have the time exactly formatted as YYYY-MM-DD HH:MM in UTC
def get_discord_timestamp(timestamp):
    try:
        if timestamp == 'now':
            dt = datetime.now(timezone.utc)
        else:
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
        
            # Make sure we are timezone aware since we know timestamp should be in UTC
            dt = dt.replace(tzinfo=timezone.utc)

        unix_timestamp = int(dt.timestamp())

        discord_timestamp = f"<t:{unix_timestamp}:F>"

        return discord_timestamp

    except ValueError:
        return "Please ensure the time is formatted properly as YYYY-MM-DD HH:MM' in UTC."


