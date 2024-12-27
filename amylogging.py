"""
Handling Amy's logging
"""

import time
import discord

class AmyLogger:
    def __init__(self):
        self.__log_file = "Logs\\amy.log"

    def __write_log(self, line: str):
        print(line)
        with open(self.__log_file, "a", encoding="utf-8") as log:
            log.write("\n" + line)

    def __time_format(self) -> str:
        return f"[{time.strftime('%Y-%m-%d %H.%M.%S', time.localtime())}]"

    def log_startup(self):
        log = f"{self.__time_format()} [STATUS  ] *yawns* Amy is waking up! >.<"
        self.__write_log(log)

    def log_quit(self):
        log = f"{self.__time_format()} [STATUS  ] *yawns* Amy is going to sleep -.-"
        self.__write_log(log)

    def log_message(self, message: discord.Message):
        log = f"{self.__time_format()} [MESSAGE ] [{message.channel}] {message.author.display_name} sent: {message.content}"
        self.__write_log(log)

    def log_response(self, message: discord.Message, response: str):
        log = f"{self.__time_format()} [RESPONSE] [{message.channel}] Amy responded to {message.author.display_name}: {response}"
        self.__write_log(log)