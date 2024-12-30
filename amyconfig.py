"""
Stores and abstracts Amy's configurable values
"""
import os
from dotenv import load_dotenv
import yaml
import time

load_dotenv()


# gpt prompts
class __OpenAIConfigs:
    def __init__(self):
        self.__API_KEY = os.getenv("OPENAI_API_KEY")
        with open("Configs/openai.yaml", 'r') as file:
            configs = yaml.safe_load(file)
            self.__prompts = configs['prompts']

    @property
    def api_key(self):
        return self.__API_KEY

    @property
    def system_prompt(self) -> str:
        return self.__prompts["system"]

    @property
    def status_prompt(self) -> str:
        return self.__prompts["status"]

    @property
    def wakeup_prompt(self) -> str:
        return self.__prompts["wakeup"]

    @property
    def time_prompt(self) -> str:
        time_format = f"{time.strftime('%H:%M, %d/%m, %Y', time.localtime())}"
        return self.__prompts["time"].format(time_format)

    @property
    def weight_prompt(self) -> str:
        return self.__prompts["weight"]


# bot permissions
class __DiscordConfigs:
    def __init__(self):
        self.__BOT_TOKEN = os.getenv("BOT_TOKEN")
        with open("Configs/discord.yaml", 'r') as file:
            configs = yaml.safe_load(file)
            self.__permissions = configs['permissions']
            self.__R = configs['response_threshold']

    @property
    def bot_token(self):
        return self.__BOT_TOKEN

    @property
    def allowed_guilds(self) -> list[int]:
        return self.__permissions["guilds"]

    @property
    def allowed_text_channels(self) -> list[int]:
        return self.__permissions["text_channels"]

    @property
    def allowed_voice_channels(self) -> list[int]:
        return self.__permissions["voice_channels"]

    @property
    def allowed_channels(self) -> list[int]:
        return self.__permissions["text_channels"] + self.__permissions["voice_channels"]

    @property
    def authorised_users(self) -> list[int]:
        return self.__permissions["users"]

    @property
    def ignored_ids(self) -> list[int]:
        return self.__permissions["ignore"]

    @property
    def response_threshold(self) -> int:
        return self.__R


open_ai_configs = __OpenAIConfigs()
discord_configs = __DiscordConfigs()
