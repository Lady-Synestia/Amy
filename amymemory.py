"""
Handling amy's memory
"""

import discord


class AmyMemory:
    def __init__(self):
        self.__memory_count = 0
        self.__remembered_interactions = []

    @property
    def memories(self):
        return self.__remembered_interactions

    @property
    def memory_count(self):
        return self.__memory_count

    def remember_interaction(self, message: discord.Message, response: str):

        self.__remembered_interactions += [
            {
                "role": "user",
                "content": message.content
            },
            {
                "role": "assistant",
                "content": response
            }
        ]

        if len(self.__remembered_interactions) > 20:
            self.__remembered_interactions.pop(0)

        self.__memory_count = len(self.__remembered_interactions)


