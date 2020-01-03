import os
import discord
import markovify
import asyncio

PREFIX = "-trevor"
TOKEN = os.environ.get("TOKEN")


def get_input_channels():
    raw = os.environ.get("INPUT_CHANNELS", "")
    channels = [int(i) for i in raw.split(",") if i != ""]
    print(f"Input Channels: {channels}")
    return channels

def get_output_channels():
    raw = os.environ.get("OUTPUT_CHANNELS", "")
    channels = [int(i) for i in raw.split(",") if i != ""]
    print(f"Output Channels: {channels}")
    return channels

def allowed_output(id):
    if len(OUTPUT_CHANNELS) == 0:
        return True
    else:
        if id in OUTPUT_CHANNELS:
            return True

    return False


def check_channel(id):
    if len(INPUT_CHANNELS) == 0:
        return True
    else:
        if id in INPUT_CHANNELS:
            return True

    return False

def add_message(m):
    global MESSAGES
    if m.content != "" and not m.author.bot and PREFIX not in m.content and check_channel(m.channel.id):
        MESSAGES += m.content + "\n"
        print("Added: 1 message to cache")

#empty array for every channel and array for one or more channels
INPUT_CHANNELS = get_input_channels()
OUTPUT_CHANNELS = get_output_channels()

client = discord.Client()
MESSAGES = ""
@client.event
async def on_ready():
    global MESSAGES
    print("Populating message cache...")
    MESSAGES = await get_messages()
    print("Done populating message cache!")


async def get_messages():
    msgs = ""
    channels = []

    if len(INPUT_CHANNELS) == 0:
        for channel in client.get_all_channels():
            if type(channel) is discord.TextChannel:
                channels.append(channel)
    else:
        for cid in INPUT_CHANNELS:
            channel = client.get_channel(cid)
            if channel and type(channel) is discord.TextChannel:
                channels.append(channel)

    for channel in channels:
        try:
            print(f"processing channel {channel.name} ...")
            messages = await channel.history(limit=10000000).flatten()
            count = 0
            for m in messages:
                if m.content != "" and not m.author.bot and PREFIX not in m.content:
                    msgs += m.content + "\n"
                    count += 1

            print(f"Added: {count} messages")
        except Exception:
            print(f"Error processing channel: {channel.name}")
    return msgs

@client.event
async def on_message(message):
    global MESSAGES
    add_message(message)
    if message.content == PREFIX and allowed_output(message.channel.id):
        try:
            text = markovify.NewlineText(MESSAGES, state_size=1)
            msg = text.make_short_sentence(2000)
            await message.channel.send(msg)
        except Exception:
            pass


@client.event
async def on_guild_join(guild):
    for channel in guild.channels:
        if type(channel) is discord.TextChannel:
            try:
                messages = await channel.history(limit=1000000).flatten()
                count = 0
                for m in messages:
                    add_message(m)
                    count += 1
                print(f"Added: {count} messages")
            except Exception:
                print("Error adding messages from new guild")


client.run(TOKEN)
