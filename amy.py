"""
Amy's controlling class
"""
import discord
from amygpt import AmyGPT
from amydiscord import AmyDiscord

class Amy:
    def __init__(self):
        self.__amy_discord = AmyDiscord()
        self.__amy_gpt = AmyGPT()

    def activate(self):
        self.__amy_discord.custom_status = self.__amy_gpt.get_new_status()
        self.__amy_discord.start_client(self.handle_discord_message)

    async def handle_discord_message(self, message: discord.Message):
        # default values
        role = "user"
        content = ""

        if message.author.id == self.__amy_discord.my_uid:
            role = "developer"
        elif message.author.display_name == "Noelle":
            content += "Message from the minecraft server: "

        content += message.content

        response = self.__amy_gpt.make_request(role, content)

        await self.__amy_discord.send_message(message.channel, response)