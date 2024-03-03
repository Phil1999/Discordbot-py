import discord
from utils.scraper import get_character_details


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
    
    MAX_USERS = 4
    MIN_USERS = 1

    valid_params = usernames and MIN_USERS <= len(usernames) <= MAX_USERS
    
    if not valid_params:
        return f"Please provide at least {MIN_USERS} username and up to {MAX_USERS} maximum. Usage: `!mrx <username> ...`", None

    character_details = []

    for username in usernames:
        curr_details = get_character_details(username)

        if curr_details['found'] is not True:
            return f"We couldn't find the character: {username}", None

        character_details.append(curr_details)
    
    # From here, we manipulate an image

    file = discord.File(f'utils\images\graph.png', filename = 'graph.png')
    embed = discord.Embed()
    title = f"{character_details[0]['name']}"

    embed.title = title
    embed.set_thumbnail(url=character_details[0]['image_url'])
    embed.set_image(url = 'attachment://graph.png')
    embed.description = "Placeholder text"
   
    return embed, file
