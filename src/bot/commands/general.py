import discord, re
from utils.scraper import get_character_details
from utils.plot import *
from datetime import datetime, timedelta
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
                "**reset+-(offset)** - (maple reset +- offset)"
                "**2023-03-15 14:00** - (Simple UTC)\n"
                "**now** - will print the current time in your timezone\n"
                "**2023-12-25T15:00:00-08:00** - (ISO 8601 format)\n"
                "**March 10 at 2pm timezone='PST'** - (The year is automatically set to current year if not specified)\n"
                "**2/24/2024 5 pm and other variations** \n"
                "**220424 at 5 pm** - (Compact dates/time) \n\n"
                "...And many more! if you think it can be interpreted as a date it likely can. \n\n"
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

    if char_exists != True:
        s = ", ".join(str(x) for x in char_exists)
        return f'The following user(s) do not exist in the database: {s}', None

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




async def get_discord_timestamp(timestamp_str, timezone_str):
    try:
        
        reset_match = re.match(r'reset([+-]\d+)?', timestamp_str.lower());

        # Special case for reset+-offset
        if reset_match:
            pacific_timezone = tz.gettz('America/Los_Angeles')

            # Get the current time in Pacific Time to determine if it's in DST
            pacific_now = datetime.now(pacific_timezone)
        
            # Determine the offset from UTC; note that .utcoffset() will return a timedelta
            # The result is negative for PST/PDT relative to UTC, so we take the absolute value
            pst_offset = abs(int(pacific_now.utcoffset().total_seconds() / 3600))

            # Maple reset is at midnight UTC
            maple_reset_time_utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
            offset_hours = int(reset_match.group(1)) if reset_match.group(1) else 0
            dt = maple_reset_time_utc + timedelta(hours=offset_hours - pst_offset)
        
        # Special case: Get the current datetime in the user-specified timezone
        elif timestamp_str.lower() == 'now':
            # If a valid timezone string is provided, use it; otherwise, default to UTC.   
            user_timezone = tz.gettz(timezone_str) if timezone_str and tz.gettz(timezone_str) else tz.UTC
            dt = datetime.now(user_timezone)
        else:
            # Parse the timestamp string, ignoring any inherent timezone information
            dt = parser.parse(timestamp_str, ignoretz=True)
            user_timezone = tz.gettz(timezone_str) if timezone_str and tz.gettz(timezone_str) else tz.UTC
            # Localize the datetime object to the user's timezone
            dt = dt.replace(tzinfo=user_timezone)
        
        # Convert the localized datetime to UTC (for generating the correct Unix timestamp)
        utc_dt = dt.astimezone(tz.UTC)

        # Generate the UNIX timestamp (should automatically be in UTC)
        unix_timestamp = int(utc_dt.timestamp())

        # Format as a Discord timestamp
        discord_timestamp = f"<t:{unix_timestamp}:F>"

        return discord_timestamp, unix_timestamp

    except ValueError:
        return "Sorry, we had trouble figuring out what you meant. Please try again.", None


