"""
Handling Amy's Discord presence
"""

import discord
import asyncio
import os
from dotenv import load_dotenv


class AmyDiscord(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

        self.__message_callback = None

        load_dotenv()
        self.__MY_UID = int(os.getenv("MY_UID"))
        self.__AMY_CHANNEL_ID = int(os.getenv("AMY_CHANNEL"))
        self.__MC_CHANNEL_ID = int(os.getenv("MC_CHANNEL"))
        self.__BOT_TOKEN = os.getenv("BOT_TOKEN")

        self.__custom_status = ""
        self.__wakeup_message = ""

    def start_client(self, message_callback, custom_status, wakeup_message):
        self.__message_callback = message_callback
        self.__custom_status = custom_status
        self.__wakeup_message = wakeup_message
        self.run(self.__BOT_TOKEN)

    async def on_ready(self):
        await self.change_presence(activity=discord.CustomActivity(self.__custom_status))
        channel = self.get_partial_messageable(self.__AMY_CHANNEL_ID)
        await channel.send(self.__wakeup_message)

    async def on_message(self, message: discord.message):
        if message.author == self.user:
            return
        if 'amy' in message.content.lower() or message.channel.type == discord.ChannelType.private or message.channel.id == self.__AMY_CHANNEL_ID:
            if message.author.id == self.__MY_UID:
                await self.__message_callback(message, role="developer")
            else:
                await self.__message_callback(message)

    async def send_message(self, channel: discord.Message.channel, message: str):
        await channel.send(message)