"""
Handling Amy's memory
"""

import discord


class AmyMemory:
    def __init__(self):
        # stores all the messages that amy remembers
        self.__max_memory_length = 5
        self._active_channels: dict[int, list] = {}

    def get_memories(self, channel_id: int) -> list[dict[str, str]]:
        """
        :return: A copy of the list of Amy's memories
        """
        if channel_id in self._active_channels:
            return self._active_channels[channel_id]
        else:
            return []

    def remember_interaction(self, message: discord.Message, response: str):
        # Custom prompt to help openai api understand the memory context
        interaction = {
            "role": "developer",
            "content": f"{message.author.global_name} said: {message.content} | you responded with: {response}"
        }

        if message.channel.id in self._active_channels:
            self._active_channels[message.channel.id].append(interaction)
        else:
            self._active_channels[message.channel.id] = [interaction]

        # caps stored memory, ensures tokens/message doesn't get too high
        if len(self._active_channels[message.channel.id]) > 5:
            self._active_channels[message.channel.id].pop(0)
