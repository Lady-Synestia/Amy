"""
Amy's controlling class

Handles communication between Amy's subcomponents
"""
import discord
from discord.ext import tasks

from amygpt import AmyGPT
from amydiscord import AmyDiscord
from amymemory import AmyMemory
import amylogging as log
import amycommands


class Amy:
    def __init__(self):
        """
        Initialising Amy's subcomponents
        """

        self.__amy_memory = AmyMemory()
        self.__amy_discord = AmyDiscord()
        self.__amy_gpt = AmyGPT()

    def activate(self):
        """
        Starts logging and wakes up discord client
        """
        log.log_startup()
        custom_status = self.__amy_gpt.get_new_status()
        wakeup_message = self.__amy_gpt.wakeup_message()

        # binds handle speech to callback for join command
        amycommands.join_callback = self.handle_join
        amycommands.say_callback = self.handle_speech
        amycommands.leave_callback = self.handle_leave
        amycommands.echo_callback = self.handle_echo
        amycommands.activity_callback = self.handle_activity_update

        self.__amy_discord.start_client(self.handle_discord_message, custom_status, wakeup_message)

    async def handle_discord_message(self, message: discord.Message, role: str = "user", vc: bool = False):
        """
        Handles link between discord and the openai api. called by discord client's on_message callback

        :param message: discord.Message object to replay as gpt message content
        :param role: role to use for gpt message role ("user", "assistant", or "developer")
        :param vc: if the bot is connected to a voice channel or not
        """

        weight = self.__amy_gpt.make_weight_request(message.content if len(message.content) < 25 else message.content[:25])
        log.log_weight(message.content, weight)
        # ensures message meets required parameters for amy to respond
        if not (abs(weight) >= 0.6 or self.__amy_discord.user in message.mentions or
                message.channel.type == discord.ChannelType.private or
                (message.reference.cached_message.author == self.__amy_discord.user if message.reference else False)):
            return

        log.log_user_message(message)

        # collecting amy's stored messages with the new message
        input_messages = self.__amy_memory.memories + [
            {
                "role": role,
                "content": message.content
            }
        ]

        # plays the discord typing animation while waiting for a response from the api
        async with message.channel.typing():
            response = self.__amy_gpt.make_chat_request(input_messages)
            await self.__amy_discord.send_message(message.channel, response)
        if vc:
            ...
            # await self.handle_speech(response)

        # saves message to amy's memory
        self.__amy_memory.remember_interaction(message, response)

    async def handle_activity_update(self, custom: str | None = None):
        if custom is None:
            custom = self.__amy_gpt.get_new_status()
        await self.__amy_discord.set_activity(custom)

    async def handle_join(self, vc: discord.VoiceClient) -> None:
        """
        Says a wakeup message when amy joins a voice channel
        :param vc: voice client connected to
        """
        self.__amy_discord.call_joined(vc)
        wakeup_message = self.__amy_gpt.wakeup_message()
        await self.handle_speech(wakeup_message)

    async def handle_leave(self) -> None:
        """
        Disconnects amy from a voice call
        """
        await self.__amy_discord.leave_call()

    async def handle_speech(self, to_say: str) -> None:
        """
        Gets a speech message from openai api, says it in the voice channel
        :param to_say: what Amy should say
        """
        file_path = self.__amy_gpt.make_voice_request(to_say)
        await self.__amy_discord.say(file_path, to_say)

    async def handle_echo(self, channel: discord.TextChannel, content: str) -> None:
        """
        echoes a message as Amy
        :param channel: channel to echo in
        :param content: message content to echo
        """
        await self.__amy_discord.send_message(channel, content)

    @tasks.loop(minutes=6)
    async def update_activity(self) -> None:
        await self.handle_activity_update()
