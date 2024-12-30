"""
Handling Amy's logging
"""

import time
import discord
import atexit


def __time_format(mode: str = "line") -> str:
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


def __write_log(line: str) -> None:
    log_file = f"Logs\\{__time_format(mode='file')}.log"
    # prints log to console and appends it to the logging file
    line = __time_format() + line
    print(line)
    with open(log_file, "a", encoding="utf-8") as log:
        log.write("\n" + line)


def log_startup() -> None:
    """
    logs startup message, called when discord client wakes up
    """
    log = f"[STATUS  ] *yawns* Amy is waking up! >.<"
    __write_log(log)


def log_quit() -> None:
    """
    logs quit event, called when the program closes
    """
    log = f"[STATUS  ] *yawns* Amy is going to sleep -.-"
    __write_log(log)


# calls log_quit() when program exits
atexit.register(log_quit)


def log_status(activity: str) -> None:
    """
    logs activity status, called when discord client wakes up
    :param activity:
    """
    log = f"[ACTIVITY] Amy set her activity to: {activity}"
    __write_log(log)


def log_user_message(message: discord.Message) -> None:
    """
    logs message sent by a user that amy will respond to
    :param message: discord.Message object containing the message
    """
    log = f"[MESSAGE ] [{message.guild}] [{message.channel}] {message.author.global_name} sent: {message.content}"
    __write_log(log)


def log_amy_reply(message: discord.Message, response: str) -> None:
    """
    logs amy's reply to a message
    :param message: discord.Message object containing the message replied to
    :param response: content of Amy's response
    """
    log = f"[REPLY   ] [{message.guild}] [{message.channel}] Amy replied to {message.author.global_name} : {response}"
    __write_log(log)


def log_amy_message(channel: discord.TextChannel, message: str) -> None:
    """
    log an original message sent by Amy
    :param channel: discord.PartialMessageable object, constructed from channel id
    :param message: message Amy sent
    """
    log = f"[MESSAGE ] [{channel.guild}] [{channel}] Amy sent: {message}"
    __write_log(log)


def log_speech(channel: discord.VoiceChannel, message: str) -> None:
    """
    log something Amy said
    :param channel: voice channel Amy spoke in
    :param message: what Amy said
    """
    log = f"[SPEECH  ] [{channel.guild}] [{channel}] Amy said: {message}"
    __write_log(log)


def log_token_usage(prompt_tokens: int, completion_tokens: int) -> None:
    """
    logs completion token usage
    :param prompt_tokens: prompt tokens used
    :param completion_tokens: completion tokens usd
    """
    log = f"[TOKENS  ] prompt tokens: {prompt_tokens} | completion tokens: {completion_tokens}"
    __write_log(log)


def log_weight(content: str, weight: float) -> None:
    """
    logs weight of checked message
    :param content: content of message
    :param weight: weight calculated
    """
    log = f"[WEIGHT  ] Message: \"{content}\" returned with weight: {weight}"
    __write_log(log)


def log_command(interaction: discord.Interaction, command: str, *args) -> None:
    """
    logs the use of an application command, including any extra arguments
    :param interaction: interaction object for the command usage
    :param command: the command used
    """
    log = f"[COMMAND ] [{interaction.guild}] [{interaction.channel}] {interaction.user.global_name} used {command}" + ("" if not args else f": {','.join(map(str, args))}")
    __write_log(log)
