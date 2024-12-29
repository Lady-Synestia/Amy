"""
Handling Amy's logging
"""

import time
import discord


class AmyLogger:
    @staticmethod
    def time_format(mode: str = "line") -> str:
        """
        defines the format time should be recorded with in the logs
        can format time for lines or filenames
        :return: string containing the current, formatted time
        """
        match mode:
            case "line":
                return f"[{time.strftime('%Y-%m-%d %H.%M.%S', time.localtime())}] "
            case "file":
                return f"{time.strftime('%d-%m-%y', time.localtime())}"

    def __write_log(self, line: str) -> None:
        log_file = f"Logs\\{self.time_format(mode='file')}.log"
        # prints log to console and appends it to the logging file
        line = self.time_format() + line
        print(line)
        with open(log_file, "a", encoding="utf-8") as log:
            log.write("\n" + line)

    def log_startup(self) -> None:
        """
        logs startup message, called when discord client wakes up
        """
        log = f"[STATUS   ] *yawns* Amy is waking up! >.<"
        self.__write_log(log)

    def log_quit(self) -> None:
        """
        logs quit event, called when the program closes
        """
        log = f"[STATUS  ] *yawns* Amy is going to sleep -.-"
        self.__write_log(log)

    def log_status(self, activity: str) -> None:
        log = f"[ACTIVITY] Amy set her activity to: {activity}"
        self.__write_log(log)

    def log_user_message(self, message: discord.Message) -> None:
        """
        logs message sent by a user that amy will respond to
        :param message: discord.Message object containing the message
        """
        log = f"[MESSAGE ] [{message.guild}] [{message.channel}] {message.author.display_name} sent: {message.content}"
        self.__write_log(log)

    def log_amy_reply(self, message: discord.Message, response: str) -> None:
        """
        logs amy's reply to a message
        :param message: discord.Message object containing the message replied to
        :param response: content of Amy's response
        """
        log = f"[REPLY   ] [{message.guild}] [{message.channel}] Amy replied to {message.author.display_name} : {response}"
        self.__write_log(log)

    def log_amy_message(self, channel: discord.PartialMessageable, message: str) -> None:
        """
        log an original message sent by Amy
        :param channel: discord.PartialMessageable object, constructed from channel id
        :param message: message Amy sent
        """
        log = f"[MESSAGE ] [{channel.guild}] [{channel.id}] Amy sent: {message}"
        self.__write_log(log)

    def log_token_usage(self, prompt_tokens: int, completion_tokens: int) -> None:
        """
        logs completion token usage
        :param prompt_tokens: prompt tokens used
        :param completion_tokens: completion tokens usd
        """
        log = f"[TOKENS  ] prompt tokens: {prompt_tokens} | completion tokens: {completion_tokens}"
        self.__write_log(log)