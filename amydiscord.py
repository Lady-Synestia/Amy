"""
Handling Amy's Discord presence
"""

import discord
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

        self.custom_status = "lil' digital cutie uwu ✨✨"

    @property
    def my_uid(self):
        return self.__MY_UID

    def start_client(self, message_callback):
        self.__message_callback = message_callback
        self.run(self.__BOT_TOKEN)

    async def on_ready(self):
        await self.change_presence(activity=discord.CustomActivity(self.custom_status))

    async def on_message(self, message: discord.message):
        if message.author == self.user:
            return
        if 'amy' in message.content.lower() or message.channel.type == discord.ChannelType.private or message.channel.id == self.__AMY_CHANNEL_ID or ( message.channel.id == self.__MC_CHANNEL_ID and message.author.display_name == "Noelle"):
            await self.__message_callback(message)

    async def send_message(self, channel: discord.Message.channel, message: str):
        await channel.send(message)