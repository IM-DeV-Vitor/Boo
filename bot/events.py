from .client import bot
from memory.context import add_message, get_context
from ai.brain import brain
from ai.vision import vision
from behavior.participation import should_participate
from behavior.moderation import is_offense
from datetime import timedelta

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content

    image_description = None

    for attachment in message.attachments:

        content_type = attachment.content_type or ""
        filename = attachment.filename.lower()

        if content_type == "image/gif" or filename.endswith(".gif"):
            image_description = await vision.describe_gif(
                attachment.url
            )
            break

        elif content_type.startswith("image/"):
            image_description = await vision.describe_image(
                attachment.url
            )
            break

    add_message(
        message.channel.id,
        str(message.author),
        content,
        is_bot=False
    )

    if is_offense(message, bot.user):
        await message.author.timeout(
            timedelta(minutes=1),
            reason="Voce ofendeu a boo!"
        )

        await message.channel.send(
            f"{message.author.mention} seu babaca!"
        )
        return

    context = get_context(message.channel.id)

    if not should_participate(message, context, bot.user):
        return

    response = await brain.generate_response(context)

    await message.channel.send(response)

    add_message(
        message.channel.id,
        str(bot.user),
        response,
        is_bot=True
    )