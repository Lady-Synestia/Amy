"""
Handling Amy's logging
"""

import time
import discord

class AmyLogger:
    def __init__(self):
        self.__log_file = "Logs\\amy.log"

    def __write_log(self, line: str):
        # prints log to console and appends it to the logging file
        print(line)
        with open(self.__log_file, "a", encoding="utf-8") as log:
            log.write("\n" + line)

    def time_format(self) -> str:
        """
        defines the format time should be recorded with in the logs
        :return: string containing the current, formatted time
        """
        return f"[{time.strftime('%Y-%m-%d %H.%M.%S', time.localtime())}]"

    def log_startup(self):
        """
        logs startup message, called when discord client wakes up
        """
        log = f"{self.time_format()} [STATUS  ] *yawns* Amy is waking up! >.<"
        self.__write_log(log)

    def log_quit(self):
        """
        logs quit event, called when the program closes
        """
        log = f"{self.time_format()} [STATUS  ] *yawns* Amy is going to sleep -.-"
        self.__write_log(log)

    def log_user_message(self, message: discord.Message):
        """
        logs message sent by a user that amy will respond to
        :param message: discord.Message object containing the message
        """
        log = f"{self.time_format()} [MESSAGE ] [{message.channel}] {message.author.display_name} sent: {message.content}"
        self.__write_log(log)

    def log_amy_reply(self, message: discord.Message, response: str):
        """
        logs amy's reply to a message
        :param message: discord.Message object containing the message replied to
        :param response: Amy's response
        """
        log = f"{self.time_format()} [RESPONSE] [{message.channel}] Amy responded to {message.author.display_name}: {response}"
        self.__write_log(log)

    def log_amy_message(self, channel: discord.PartialMessageable, message: str):
        """
        log an original message sent by Amy
        :param channel: discord.PartialMessageable object, constructed from channel id
        :param message: message Amy sent
        """
        log = f"{self.time_format()} [MESSAGE ] [{channel.name}] Amy sent: {message}"
        self.__write_log(log)