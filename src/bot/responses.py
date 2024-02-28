# bot/responses.py
from .commands import general

def handle_response(message) -> str:
    p_message = message.lower()

    command_map = {
        'hello': general.hello,
        '!help': general.help,
    }

    if p_message in command_map:
        return command_map[p_message]()
    else:
        return "Sorry, I didn't understand that command."
