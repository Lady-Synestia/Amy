"""
Handling Amy's Discord presence
"""

import discord
from discord import app_commands
from amylogging import AmyLogger
import amycommands
from typing import Callable
from amyconfig import BOT_TOKEN, permissions


class AmyDiscord(discord.Client):
    __custom_status: str
    __wakeup_message: str

    __message_callback: Callable

    __voice_client: discord.VoiceClient | None

    def __init__(self, logger: AmyLogger):
        self.__amy_logger = logger

        # setting up bot intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(intents=intents)

        # stores application commands to be synced with discord
        self.__tree = app_commands.CommandTree(self)

    def start_client(self, message_callback, custom_status, wakeup_message):
        """
        Runs the discord client and handles post-initialisation of parameters
        """
        self.__message_callback = message_callback
        self.__custom_status = custom_status
        self.__wakeup_message = wakeup_message

        # adding application commands to be synced with discord
        # guild/guilds must be satisfied for commands to be registered straight away
        my_guilds = [discord.Object(id=guild) for guild in permissions.guilds]
        self.__tree.add_command(amycommands.join, guilds=my_guilds)
        self.__tree.add_command(amycommands.say, guilds=my_guilds)
        self.__tree.add_command(amycommands.leave, guilds=my_guilds)
        self.__tree.add_command(amycommands.echo, guilds=my_guilds)

        self.run(BOT_TOKEN)

    async def send_message(
            self,
            channel: discord.TextChannel | discord.PartialMessageable | discord.DMChannel | discord.GroupChannel,
            message: str):
        """
        Allows Amy to send a message
        :param channel: the channel to respond in
        :param message: message to send
        """
        await channel.send(message)
        self.__amy_logger.log_amy_message(channel, message)

    async def reply(self, message: discord.Message, content: str, mention: bool = False):
        """
        Allows Amy to reply to a message
        :param message: discord.Message object to reply to
        :param content: contents of the reply
        :param mention: whether to mention the user or not, defaults to False
        """
        await message.reply(content, mention_author=mention)
        self.__amy_logger.log_amy_reply(message, content)

    async def say(self, file_path: str, transcript: str) -> None:
        if self.__voice_client is not None:
            source = discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe", source=file_path)
            self.__voice_client.play(source)
            self.__amy_logger.log_speech(self.__voice_client.channel, transcript)

    def call_joined(self, vc: discord.VoiceClient):
        self.__voice_client = vc

    async def leave_call(self):
        if self.__voice_client is not None:
            await self.__voice_client.disconnect()
            self.__voice_client = None

    async def on_ready(self):
        """
        Discord client event: called when bot is ready
        """
        await self.__tree.sync(guild=discord.Object(id=permissions.guilds[0]))

        await self.change_presence(activity=discord.CustomActivity(self.__custom_status))
        self.__amy_logger.log_status(self.__custom_status)
        channel = self.get_partial_messageable(permissions.text_channels[0])
        # await self.send_message(channel, self.__wakeup_message)

    async def on_message(self, message: discord.message):
        """
        Discord client event: called when a message is sent in a guild or dm that Amy is in
        :param message: discord.Message object containing the message
        """

        # prevents Amy from responding to her own messages
        if message.author == self.user or message.channel.id in permissions.ignore:
            return

        await self.__message_callback(message)

        # ensures message meets required parameters for amy to respond
        # if (self.user in message.mentions or
        #         message.channel.type == discord.ChannelType.private or
        #         message.channel.id in permissions.text_channels or
        #         (message.reference.cached_message.author == self.user if message.reference else False)):
        #     self.__amy_logger.log_user_message(message)
        #     await self.__message_callback(message, vc=(message.channel.id == permissions.voice_channels[0]))
