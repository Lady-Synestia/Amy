"""
Handling Amy's Discord presence
"""

import discord
from discord import app_commands
import asyncio
import os
from dotenv import load_dotenv


class AmyDiscord(discord.Client):
    def __init__(self):
        load_dotenv()
        self.__MY_UID = int(os.getenv("MY_UID"))
        self.__AMY_CHANNEL_ID = int(os.getenv("AMY_CHANNEL"))
        self.__MC_CHANNEL_ID = int(os.getenv("MC_CHANNEL"))
        self.__BOT_TOKEN = os.getenv("BOT_TOKEN")

        # setting up bot intents
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

        # function callback for on_message event
        self.__message_callback = None

        self.__custom_status = ""
        self.__wakeup_message = ""

    def start_client(self, message_callback, custom_status, wakeup_message):
        """
        Runs the discord client and handles post-initialisation of parameters
        """
        self.__message_callback = message_callback
        self.__custom_status = custom_status
        self.__wakeup_message = wakeup_message
        self.run(self.__BOT_TOKEN)

    async def on_ready(self):
        """
        Discord client event: called when bot is ready
        """

        await self.change_presence(activity=discord.CustomActivity(self.__custom_status))
        channel = self.get_partial_messageable(self.__AMY_CHANNEL_ID)
        await self.send_message(channel, self.__wakeup_message)

    async def on_message(self, message: discord.message):
        """
        Discord client event: called when a message is sent in a guild or dm that Amy is in
        :param message: discord.Message object containing the message
        """

        # prevents Amy from responding to her own messages
        if message.author == self.user:
            return

        # ensures message meets required parameters for amy to respond
        # * TODO: improve this and store parameters in a smarter way
        if 'amy' in message.content.lower() or message.channel.type == discord.ChannelType.private or message.channel.id == self.__AMY_CHANNEL_ID:
            await self.__message_callback(message)

    async def send_message(self, channel: discord.Message.channel | discord.PartialMessageable, message: str):
        """
        Allows Amy to send a message
        :param channel: the channel to respond in
        :param message: message to send
        """
        await channel.send(message)

    async def reply(self, message: discord.Message, content: str):
        """
        Allows Amy to reply to a message
        :param message: discord.Message object to reply to
        :param content: contents of the reply
        """
        await message.reply(content)