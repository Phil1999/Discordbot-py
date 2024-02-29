from .commands import general
import asyncio

async def handle_response(message):
    p_message = message.content.lower().strip()
    trimmed_message = p_message[1:] # Remove the ! or ?

    command_map = {
        'hello': general.hello,
        'help': general.help,
        'image': general.send_image_url
    }

    command_func = command_map.get(trimmed_message)

    if command_func:
        if asyncio.iscoroutinefunction(command_func):
            return await command_func()
        else:
            return command_func()
    else:
        return "Sorry, I couldn't understand the command"
    
