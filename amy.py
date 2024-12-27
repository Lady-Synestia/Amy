# This example requires the 'message_content' intent.
import os
from dotenv import load_dotenv
import discord

load_dotenv()
MY_UID = int(os.getenv("MY_UID"))
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('hi amy'):
        if message.author.id == MY_UID:
            await message.channel.send(f'hi mum!! >.<')
        else:
            await message.channel.send(f'hiiii <@{message.author.id}>! >//w//<')
    elif "bye" in message.content.lower():
        await message.channel.send("byeeeee!!")

client.run(BOT_TOKEN)
