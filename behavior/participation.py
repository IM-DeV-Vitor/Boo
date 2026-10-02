import random

def should_participate(message, context, bot_user):
    if bot_user in message.mentions:
        return True

    bot_name = bot_user.name.lower()
    content = message.content.lower()

    if bot_name in content:
        return True

    if len(context) < 2:
        return False

    return random.random() < 0.08