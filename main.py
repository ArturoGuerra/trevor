import os
import discord
import markovify
import asyncio

PREFIX = "-trevor"
TOKEN = os.environ.get("TOKEN")
MSG_CHANNEL = 658866785466187787

client = discord.Client()
MESSAGES = ""
@client.event
async def on_ready():
    global MESSAGES
    print("Populating messages cache...")
    MESSAGES = await get_messages()
    await asyncio.sleep(100000)


async def get_messages():
    msgs = ""
    channel = client.get_channel(MSG_CHANNEL)
    if not channel:
        return ""

    messages = await channel.history(limit=10000000).flatten()

    count = 0
    for m in messages:
        if m.content != "" and not m.author.bot and PREFIX not in m.content:
            msgs += m.content + "\n"
            count += 1

    print(f"Added: {count} messages")
    return msgs





@client.event
async def on_message(message):
    global MESSAGES
    if message.content == PREFIX:
        try:
            text = markovify.NewlineText(MESSAGES, state_size=1)
            msg = text.make_short_sentence(140)
            await message.channel.send(msg)
        except Exception:
            pass
    else:
        add_message(message)

def add_message(m):
    global MESSAGES
    if m.content != "" and not m.author.bot and PREFIX not in m.content and m.channel.id == MSG_CHANNEL:
        MESSAGES += m.content + "\n"
        print("Added: 1 message to cache")

client.run(TOKEN)
