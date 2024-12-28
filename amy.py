"""
Amy's controlling class
"""
import discord
import atexit
from amygpt import AmyGPT
from amydiscord import AmyDiscord
from amylogging import AmyLogger
from amymemory import AmyMemory

class Amy:
    def __init__(self):
        self.__amy_logger = AmyLogger()
        atexit.register(self.__amy_logger.log_quit)
        self.__amy_memory = AmyMemory()
        self.__amy_discord = AmyDiscord()
        self.__amy_gpt = AmyGPT()

    def activate(self):
        self.__amy_logger.log_startup()
        custom_status = self.__amy_gpt.get_new_status()
        wakeup_message = self.__amy_gpt.wakeup_message()
        self.__amy_discord.start_client(self.handle_discord_message, custom_status, wakeup_message)

    async def handle_discord_message(self, message: discord.Message):
        self.__amy_logger.log_message(message)

        input_messages = self.__amy_memory.memories + [
            {
                "role": "user",
                "content": message.content
            }
        ]

        async with message.channel.typing():
            response = self.__amy_gpt.make_request(input_messages)
            await self.__amy_discord.send_message(message.channel, response)

        self.__amy_logger.log_response(message, response)
        self.__amy_memory.remember_interaction(message, response)