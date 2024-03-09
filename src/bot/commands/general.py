import discord
from utils.scraper import get_character_details
from utils.plot import *

def hello():
    return "Hello World"

def help():
    return "Help message..."

async def send_image_url():
    embed = discord.Embed(
        title="Test Image",
        description="This is a test image",
    )
    embed.set_image(url="https://pngimg.com/uploads/spongebob/spongebob_PNG58.png")

    return embed

async def send_character_image_url(usernames):
    
    NUM_USERS = len(usernames)

    MAX_USERS = 4
    MIN_USERS = 1

    valid_params = usernames and MIN_USERS <= len(usernames) <= MAX_USERS
    
    if not valid_params:
        return f"Please provide at least {MIN_USERS} username and up to {MAX_USERS} maximum. Usage: `!mrx <username> ...`", None

    comparison(get_data(), usernames)
    file = discord.File(f'assets/images/graph.png', filename = 'graph.png')

    if NUM_USERS == 1:
        character_details = get_character_details(usernames[0])
        print(character_details)
        embed = discord.Embed()
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
    
   
