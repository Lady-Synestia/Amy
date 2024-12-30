"""
Handling Amy's memory
"""

import discord


class AmyMemory:
    def __init__(self):
        # stores all the messages that amy remembers
        self.__remembered_interactions = []

    @property
    def memories(self) -> list[dict[str,str]]:
        """
        :return: A copy of the list of Amy's memories
        """
        return self.__remembered_interactions

    @property
    def memory_count(self):
        """
        :return: Number of memories Amy has
        """
        return len(self.__remembered_interactions)

    def remember_interaction(self, message: discord.Message, response: str):
        # Custom prompt to help openai api understand the memory context
        self.__remembered_interactions += [
            {
                "role": "developer",
                "content": f"{message.author.global_name} said: {message.content} | you responded with: {response}"
            }
        ]

        # caps stored memory, ensures tokens/message doesn't get too high
        if self.memory_count > 5:
            self.__remembered_interactions.pop(0)
