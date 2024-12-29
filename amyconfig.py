"""
Stores and abstracts Amy's configurable values
"""
import dataclasses
import os
from dotenv import load_dotenv
import yaml
import time


# gpt prompts
class __Prompts():
    def __init__(self):
        with open("Configs\\config.yaml", 'r') as file:
            configs = yaml.safe_load(file)
            self.__prompts = configs['Prompts']

    @property
    def system(self) -> str:
        return self.__prompts["system"]

    @property
    def status(self) -> str:
        return self.__prompts["status"]

    @property
    def wakeup(self) -> str:
        return self.__prompts["wakeup"]

    @property
    def time(self) -> str:
        time_format = f"{time.strftime('%H:%M, %d/%m, %Y', time.localtime())}"
        return self.__prompts["time"].format(time_format)

    @property
    def weight(self) -> str:
        return self.__prompts["weight"]


# bot permissions
class __Permissions():
    def __init__(self):
        with open("Configs\\config.yaml", 'r') as file:
            configs = yaml.safe_load(file)
            self.__permissions = configs['Permissions']

    @property
    def guilds(self) -> list[int]:
        return self.__permissions["guilds"]

    @property
    def text_channels(self) -> list[int]:
        return self.__permissions["text_channels"]

    @property
    def voice_channels(self) -> list[int]:
        return self.__permissions["voice_channels"]

    @property
    def users(self) -> list[int]:
        return self.__permissions["users"]

    @property
    def ignore(self) -> list[int]:
        return self.__permissions["ignore"]


# environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENAI_API_KEY")

prompts = __Prompts()
permissions = __Permissions()






