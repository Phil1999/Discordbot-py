


def handle_response(message) -> str:
    p_message = message.lower()

    responses = {
        'hello': 'Hello World',
        '!help': 'Help message',
        # Can add new commands here
    }

    # Default response if command is not recognized
    default_response = "Sorry, I didn't understand that command."

    # Return the response if the command is known, else return the default response
    return responses.get(p_message, default_response)
