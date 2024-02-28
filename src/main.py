import os
from bot.core import init_discord_bot
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    discord_token = os.getenv('DISCORD_TOKEN')
    init_discord_bot(discord_token)