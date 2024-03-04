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

    character_details = get_character_details(usernames[0])

    # From here, we manipulate an image
    userGraph(get_data(), usernames)

    file = discord.File(f'assets/images/graph.png', filename = 'graph.png')
    embed = discord.Embed()
    title = f"{character_details['name']}"

    embed.title = title

    # For thumbnail, use the composite image
    embed.set_thumbnail(url= f'{character_details['image_url']}')
    # TODO: for more than 1 person we don't display a thumbnail.
    embed.set_image(url = 'attachment://graph.png')
    embed.description = "Placeholder text"
    
    return embed, file
