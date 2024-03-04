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
        embed = discord.Embed()
        title = f"{character_details['name']}"
        embed.title = title
        embed.set_thumbnail(url=character_details['image_url'])

        stat_dict = stats(get_data(), usernames[0])

        percent = float(str(stat_dict['ptcp']).replace('%',''))
        if percent == 100.0:
            padding = 28
        elif percent > 9.99:
            padding = 27
        else:
            padding = 25
        print(padding)
        line = '-' * padding
        des = (
            line + '\n' + 
            'Participation Rate: ' + str(stat_dict['ptcp']) + '%' + '\n' + 
            'Min: ' + str(stat_dict['min']) + '\n' + 
            'Average: ' + str(stat_dict['mean']) + '\n' + 
            'Max: ' + str(stat_dict['max']) + '\n' + 
            line
        )
        embed.description = des
        embed.set_image(url = 'attachment://graph.png')
        return embed, file
    else:
        return None, file
    

    
    
    

    

    

    
    
    return embed, file
   
