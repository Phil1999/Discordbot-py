import discord
from utils.scraper import get_character_details
from utils.plot import *
from datetime import datetime
from dateutil import parser, tz

embed_side_color = discord.Color.blue() 
separator = chr(173) # two line separator


async def floppy():
    embed = discord.Embed()
    
    floppy_url = "https://media1.tenor.com/m/oBNwHVvVBawAAAAd/flacid-stick-shift.gif"

    embed.set_image(url=floppy_url)

    return embed


def help():
    embed = discord.Embed()
    embed.color = embed_side_color 
    embed.title = "*Commands*"
    embed.set_footer(text= "Schulich Bot")
    
     
    embed.add_field(
        name="Culvert",
        value=(
            "\n`/gpq [names], optional 'num_weeks (num)'` \n"
            "Enter a **single** username to receive an image of their Culvert score.\n"
            "For **2-4** usernames, you will receive a comparative graph image against all listed players.\n"
            "Enter the optional param `num_weeks` to show the last **'num'** weeks of culvert scores. \n\n"
            "*Note: \nA maximum of **4** usernames can be entered.*"
        ),
        inline=False
    )
    
    embed.add_field(name=separator, value="")

    embed.add_field(
        name="Discord Timestamp",
        value=(
            "\n`/converttime (timestamp), or 'now' for the current time` \n"
                "**Enter a timestamp and optionally specify the timezone to convert it into a Discord timestamp.**\n\n"
                "Accepted Formats for timestamp: \n"
                "**2023-03-15 14:00** - (Simple UTC)\n"
                "**now** - will print the current time in your timezone\n"
                "**2023-12-25T15:00:00-08:00** - (ISO 8601 format)\n"
                "**March 10 at 2pm timezone='PST'** - (The year is automatically generated if not specified)\n\n"
                "*Note: \nTimezones must follow a format such as: **(PST or Asia/Tokyo)** exactly.*"
        ),
        inline=False
    )

    embed.add_field(name=separator, value="")


    embed.add_field(
        name="Floppy",
        value=
            "\n`/floppy`\n"
            ":susge: \n"
        ,
        inline=False
    )

    embed.add_field(name=separator, value="")

    embed.add_field(
        name="Schulich Help",
        value="\n`/help` \n" + "Shows this message.", 
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
            char_exists = comparison(get_data(), usernames, num_weeks)
    else:
        char_exists = comparison(get_data(), usernames, None)

    if char_exists == False:
        return 'This user does not exist in the database', None
    
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
        if stat_dict['rank'] == None:
            embed.set_footer(text='User did not run last week')
        else:
            embed.set_footer(text=f'Rank #{stat_dict["rank"]} of {stat_dict["numptcp"]} in the most recent week')
        embed.add_field(name='Participation (%)', value = stat_dict['ptcp'], inline = False)
        embed.add_field(name='Min', value = stat_dict['min'], inline = True)
        embed.add_field(name='Average', value = stat_dict['mean'], inline = True)
        embed.add_field(name='Max', value = stat_dict['max'], inline = True)
        embed.set_image(url = 'attachment://graph.png')
        return embed, file
    else:
        return None, file

async def get_discord_timestamp(timestamp_str, timezone_str):
    try:
            
        # If a valid timezone string is provided, use it; otherwise, default to UTC.
        user_timezone = tz.gettz(timezone_str) if timezone_str and tz.gettz(timezone_str) is not None else tz.UTC
        
        # Handle the special case where the timestamp is 'now'.
        if timestamp_str.lower() == 'now':
            dt = datetime.now(user_timezone)
        else:
            # Parse the timestamp string.
            dt = parser.parse(timestamp_str)

            # If the datetime object parsed does not have timezone info, use the provided/default timezone.
            if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
                dt = dt.replace(tzinfo=user_timezone)
            else:
                # Convert the datetime to the specified timezone to reflect the user's local time.
                dt = dt.astimezone(user_timezone)

        # Generate the UNIX timestamp and format it as a Discord timestamp.
        unix_timestamp = int(dt.timestamp())
        discord_timestamp = f"<t:{unix_timestamp}:F>"

        return discord_timestamp, unix_timestamp

    except ValueError:
        return "Sorry, we had trouble figuring out what you meant. Please try again.", None


