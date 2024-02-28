import bot, os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    discord_token = os.getenv('DISCORD_TOKEN')
    bot.init_discord_bot(discord_token)