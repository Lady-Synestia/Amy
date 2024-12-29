"""
Amy's controlling class

Handles communication between Amy's subcomponents
"""
import discord
import atexit
from amygpt import AmyGPT
from amydiscord import AmyDiscord
from amylogging import AmyLogger
from amymemory import AmyMemory
import amycommands


class Amy:
    def __init__(self):
        """
        Initialising Amy's subcomponents
        """
        self.__amy_logger = AmyLogger()
        atexit.register(self.__amy_logger.log_quit)

        self.__amy_memory = AmyMemory()
        self.__amy_discord = AmyDiscord(self.__amy_logger)
        self.__amy_gpt = AmyGPT(self.__amy_logger)

    def activate(self):
        """
        Starts logging and wakes up discord client
        """
        self.__amy_logger.log_startup()
        custom_status = self.__amy_gpt.get_new_status()
        wakeup_message = self.__amy_gpt.wakeup_message()

        # binds handle speech to callback for join command
        amycommands.join_callback = self.handle_join
        amycommands.speech_callback = self.handle_speech

        self.__amy_discord.start_client(self.handle_discord_message, custom_status, wakeup_message)

    async def handle_discord_message(self, message: discord.Message, role: str = "user", vc: bool = False):
        """
        Handles link between discord and the openai api. called by discord client's on_message callback

        :param message: discord.Message object to replay as gpt message content
        :param role: role to use for gpt message role ("user", "assistant", or "developer")
        """

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
            await self.__amy_discord.reply(message, response)
        if vc:
            ...
            # await self.handle_speech(response)

        # saves message to amy's memory
        self.__amy_memory.remember_interaction(message, response)

    async def handle_join(self, voice_client) -> None:
        """
        Says a wakeup message when amy joins a voice channel
        :param voice_client: voice client connected to
        """
        self.__amy_discord.current_voice_client = voice_client
        wakeup_message = self.__amy_gpt.wakeup_message()
        await self.handle_speech(wakeup_message)

    async def handle_speech(self, to_say: str) -> None:
        """
        Gets a speech message from openai api, says it in the voice channel
        :param to_say: what Amy should say
        """
        file_path = self.__amy_gpt.make_voice_request(to_say)
        await self.__amy_discord.say(file_path, to_say)
