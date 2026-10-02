from collections import defaultdict, deque

MAX_MESSAGES = 20

conversations = defaultdict(lambda: deque(maxlen=MAX_MESSAGES))

def add_message(channel_id, author, content, is_bot=False):
    conversations[channel_id].append({
        'author': author,
        'content': content,
        'is_bot': is_bot
    })

def get_context(channel_id):
    return list(conversations[channel_id])

def get_context_text(channel_id):
    messages = get_context(channel_id)

    return '\n'.join(
        f"{message['author']}: {message['content']}"
        for message in messages
    )