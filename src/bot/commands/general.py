import discord, re
from utils.scraper import get_character_details
from utils.plot import *
from utils.sheets import *
from datetime import datetime, timedelta
from dateutil import parser, tz
import dateparser
from zoneinfo import ZoneInfo

embed_side_color = discord.Color.blue() 
separator = chr(173) # two line separator


async def floppy():
    file = discord.File(f'assets/images/floppy.gif', filename = 'floppy.gif')
    return file


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
                "**March 10 at 2pm timezone='PST'** - (The year is automatically set to current year if not specified)\n"
                "**2/24/2024 5 pm and other variations** \n"
                "**220424 at 5 pm** - (Compact dates/time) \n"
                "**in 2 hours** - (relative times)\n\n"
                "...And many more! if you think it can be interpreted as a date it likely can. \n\n"
                "*Note: \nTimezones must follow a format such as: **(PST or Asia/Tokyo)** exactly.*\n"
                "For the highest degree of accuracy, follow a standard format as much as possible\n"
                "**now** is a timezone independent calculations. You do not need to put a timezone\n"
                "Default timezone is UTC \n\n"
        ),
        inline=False
    )

    embed.add_field(name=separator, value="")


    embed.add_field(
        name="Floppy",
        value=
            "\n`/floppy`\n"
            "<:susge:1174732518839304306> \n"
        ,
        inline=False
    )

    embed.add_field(name=separator, value="")

    embed.add_field(
        name="Schulich Help",
        value="\n`/help` \n" + "Shows this message.", 
        inline=False
    )

 
    return embed


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
        if stat_dict['rank'] != None:
            embed.set_footer(text='Rank #' + str(stat_dict['rank']) + ' of ' + str(stat_dict['numptcp']) + ' in most recent week')
        else:
            embed.set_footer(text='User did not run last week')
        embed.add_field(name='Participation (%)', value = stat_dict['ptcp'], inline = False)
        embed.add_field(name='Min', value = stat_dict['min'], inline = True)
        embed.add_field(name='Average', value = stat_dict['mean'], inline = True)
        embed.add_field(name='Max', value = stat_dict['max'], inline = True)
        embed.set_image(url = 'attachment://graph.png')
        return embed, file
    else:
        return None, file


timezone_mapping = {
    'PST': 'America/Los_Angeles',  # Pacific Standard Time
    'PDT': 'America/Los_Angeles',  # Pacific Daylight Time
    'MST': 'America/Denver',       # Mountain Standard Time
    'MDT': 'America/Denver',       # Mountain Daylight Time
    'CST': 'America/Chicago',      # Central Standard Time
    'CDT': 'America/Chicago',      # Central Daylight Time
    'EST': 'America/New_York',     # Eastern Standard Time
    'EDT': 'America/New_York',     # Eastern Daylight Time
}

# Helper method to map abbreviations to pytz identifier, defaults to UTC if not found.
def get_correct_timezone(tz_str):
    return ZoneInfo(timezone_mapping.get(tz_str, 'UTC'))

def normalize_time_format(time_str):
    time_str = re.sub(r'(?P<hour>\d{1,2})(?P<minute>\d{2})(am|pm)', r'\g<hour>:\g<minute>\3', time_str, flags=re.IGNORECASE)

    return time_str

async def get_discord_timestamp(timestamp_str, timezone_str):
    try:
        reset_pattern = r'reset(?:\s*([+-]?\s*\d+(?:\.\d+)?))?(?:\s*hours?)?'
        reset_match = re.match(reset_pattern, timestamp_str, flags=re.IGNORECASE)
     
        utc_timezone = ZoneInfo("UTC")

         # Timezone logic
        if timezone_str:
            if timezone_str.upper() in timezone_mapping:
                user_timezone = get_correct_timezone(timezone_str.upper()) # Let users input pst, est, ...etc
            else:
                try:
                    user_timezone = ZoneInfo(timezone_str) # But, for canonical timezones it must match exactly
                except Exception:
                    return "Sorry we had trouble figuring out what timezone you meant. Please try again.", None
        else:
            user_timezone = utc_timezone


        # Special case for reset+-offset
        if reset_match:
            # Remove whitespace so we can parse 
            offset_str = reset_match.group(1).replace(" ", "") if reset_match.group(1) else "0" 
            offset_hours = float(offset_str)
            
            # Calculate the hours/minutes
            full_hours = int(offset_hours)
            minutes = int((offset_hours - full_hours) * 60)

            # Maple reset is at midnight UTC, since we reset to 00:00:00 of current day add 24 hours.
            maple_reset_time_utc = datetime.now(utc_timezone).replace(hour=0, minute=0, second=0, microsecond=0) 
        
            dt = maple_reset_time_utc + timedelta(hours=full_hours, minutes=minutes)
        
        else:
           

            normalized_str = normalize_time_format(timestamp_str)
            # Parse the timestamp string using dateparser first
            dt = dateparser.parse(normalized_str, languages=['en'], settings={'TIMEZONE': str(user_timezone), 'RETURN_AS_TIMEZONE_AWARE' : True})
            
            # Otherwise, try dateutils.parse
            if not dt:
                dt = parser.parse(normalized_str)


            # We received a naive datetime if this is true
            if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
                dt = dt.replace(tzinfo=user_timezone)
            
            else:
                # We received a timestamp with the string in it

                # If we received a specific timezone to parse it as
                    if timezone_str:
                        dt = dt.astimezone(user_timezone)
                
        # Convert the localized datetime to UTC (for generating the correct Unix timestamp)
        utc_dt = dt.astimezone(utc_timezone)

        # Generate the UNIX timestamp (should automatically be in UTC)
        unix_timestamp = int(utc_dt.timestamp())

        # Format as a Discord timestamp
        discord_timestamp = f"<t:{unix_timestamp}:F>"

        return discord_timestamp, unix_timestamp

    except ValueError:
        return "Sorry, we had trouble figuring out what you meant. Please try again.", None


async def save_csv(attachment: discord.Attachment):
        
     # Reading attachments
    if attachment:
        file = attachment

        if not file.filename.endswith('csv'):
            return "Please send a .csv file"


        save_path = "assets/data"
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_saved_name = "data.csv"
        file_path = os.path.join(save_path, file_saved_name)

        await file.save(file_path)

        export_valid = await csv_to_sheets()
        if export_valid:
            update_valid = await update_data()
        else:
            return "It is too early to update culvert data."
        
        if update_valid:
            return "Data update was successful."
        else:
            return "Data update was unsuccessful."



     

