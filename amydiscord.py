"""
Handling Amy's Discord presence
"""

import discord
from discord import app_commands
import amylogging as log
import amycommands
from typing import Callable
from amyconfig import discord_configs as configs


class AmyDiscord(discord.Client):
    __custom_status: str
    __wakeup_message: str

    __message_callback: Callable
    __status_callback: Callable

    __voice_client: discord.VoiceClient | None

    def __init__(self):
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
        my_guilds = [discord.Object(id=guild) for guild in configs.allowed_guilds]
        self.__tree.add_command(amycommands.join, guilds=my_guilds)
        self.__tree.add_command(amycommands.say, guilds=my_guilds)
        self.__tree.add_command(amycommands.leave, guilds=my_guilds)
        self.__tree.add_command(amycommands.echo, guilds=my_guilds)
        self.__tree.add_command(amycommands.activity, guilds=my_guilds)
        self.__tree.add_command(amycommands.r, guilds=my_guilds)

        self.run(configs.bot_token)

    async def set_activity(self, status: str, activity_type: discord.ActivityType | None = None, ) -> None:
        """
        sets Amy's activity, can be custom or have a type
        :param status: activity status or name
        :param activity_type: type of activity, if none will be a custom activity
        """
        self.__custom_status = status
        if activity_type is not None:
            await self.change_presence(activity=discord.Activity(type=activity_type, name=status))
        else:
            await self.change_presence(activity=discord.CustomActivity(status))
        log.log_status(self.__custom_status)

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
        log.log_amy_message(channel, message)

    async def reply(self, message: discord.Message, content: str, mention: bool = False):
        """
        Allows Amy to reply to a message
        :param message: discord.Message object to reply to
        :param content: contents of the reply
        :param mention: whether to mention the user or not, defaults to False
        """
        await message.reply(content, mention_author=mention)
        log.log_amy_reply(message, content)

    async def say(self, file_path: str, transcript: str) -> None:
        if self.__voice_client is not None:
            source = discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe", source=file_path)
            self.__voice_client.play(source)
            log.log_speech(self.__voice_client.channel, transcript)

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
        await self.__tree.sync(guild=discord.Object(id=configs.allowed_guilds[0]))

        await self.set_activity(self.__custom_status)
        # channel = self.get_partial_messageable(permissions.text_channels[0])
        # await self.send_message(channel, self.__wakeup_message)

    async def on_message(self, message: discord.message):
        """
        Discord client event: called when a message is sent in a guild or dm that Amy is in
        :param message: discord.Message object containing the message
        """

        # prevents Amy from responding to her own messages
        if (message.author == self.user or
                message.channel.id in configs.ignored_ids or
                message.author.id in configs.ignored_ids):
            return

        await self.__message_callback(message)
