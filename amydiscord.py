"""
Handling Amy's Discord presence
"""

import discord
from discord import app_commands
from amylogging import AmyLogger
import amycommands
from amyconfig import AMY_CHANNEL, BOT_TOKEN, AMY_GUILD, VC_CHANNEL


class AmyDiscord(discord.Client):
    def __init__(self, logger: AmyLogger):
        self.__amy_logger = logger

        # setting up bot intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(intents=intents)

        # stores application commands to be synced with discord
        self.__tree = app_commands.CommandTree(self)

        # function callback for on_message event
        self.__message_callback = None

        self.current_voice_client = None

    def start_client(self, message_callback, custom_status, wakeup_message):
        """
        Runs the discord client and handles post-initialisation of parameters
        """
        self.__message_callback = message_callback
        self.__custom_status = custom_status
        self.__wakeup_message = wakeup_message

        # adding application commands to be synced with discord
        # guild/guilds must be satisfied for commands to be registered straight away
        self.__tree.add_command(amycommands.test, guild=discord.Object(id=AMY_GUILD))
        self.__tree.add_command(amycommands.join, guild=discord.Object(id=AMY_GUILD))
        self.__tree.add_command(amycommands.say, guild=discord.Object(id=AMY_GUILD))

        self.run(BOT_TOKEN)

    async def on_ready(self):
        """
        Discord client event: called when bot is ready
        """
        await self.__tree.sync(guild=discord.Object(id=AMY_GUILD))

        await self.change_presence(activity=discord.CustomActivity(self.__custom_status))
        self.__amy_logger.log_status(self.__custom_status)
        channel = self.get_partial_messageable(AMY_CHANNEL)
        await self.send_message(channel,self.__wakeup_message)

    async def on_message(self, message: discord.message):
        """
        Discord client event: called when a message is sent in a guild or dm that Amy is in
        :param message: discord.Message object containing the message
        """

        # prevents Amy from responding to her own messages
        if message.author == self.user:
            return

        # ensures message meets required parameters for amy to respond
        # TODO: improve this and store parameters in a smarter way
        if 'amy' in message.content.lower() or message.channel.type == discord.ChannelType.private or message.channel.id == AMY_CHANNEL:
            self.__amy_logger.log_user_message(message)
            await self.__message_callback(message, vc = (message.channel.id == VC_CHANNEL))

    async def send_message(self, channel: discord.TextChannel | discord.PartialMessageable | discord.DMChannel | discord.GroupChannel, message: str):
        """
        Allows Amy to send a message
        :param channel: the channel to respond in
        :param message: message to send
        """
        await channel.send(message)
        self.__amy_logger.log_amy_message(channel, message)

    async def reply(self, message: discord.Message, content: str):
        """
        Allows Amy to reply to a message
        :param message: discord.Message object to reply to
        :param content: contents of the reply
        """
        await message.reply(content, mention_author=False)
        self.__amy_logger.log_amy_reply(message, content)

    async def say(self, file_path: str, transcript: str) -> None:
        source = discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe", source=file_path)
        self.current_voice_client.play(source)
        self.__amy_logger.log_speech(self.current_voice_client.channel, transcript)
