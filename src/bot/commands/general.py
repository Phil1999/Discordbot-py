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

async def send_character_image_url(username):

    if username is None:
        return "Please provide a username. Usage: `!mrx <username>`"

    character_details = get_character_details(username)

    if not character_details['found']:
        return "We couldn't find that character."
    
    embed = discord.Embed()
    title = f"{character_details['name']}"

    embed.title = title
    embed.set_thumbnail(url=character_details['image_url'])
    embed.set_image(url="https://pngimg.com/uploads/spongebob/spongebob_PNG58.png")
    embed.description = f"{character_details.get('level_percentage')} {character_details.get('class_and_world')}"

    return embed
