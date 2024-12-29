"""
Handling Amy's GPT-4o-mini completions
"""

import time
from openai import OpenAI
from amylogging import AmyLogger
from amyconfig import API_KEY, SYSTEM_PROMPT, STATUS_PROMPT, WAKEUP_PROMPT


class AmyGPT:
    def __init__(self, logger: AmyLogger):

        self.__amy_logger = logger

        self.__system_message = self.completion_message("developer", SYSTEM_PROMPT)

        self.__time_message = self.completion_message("developer",
                                                      f"The current time (hour:minute, day/month), year is: {time.strftime('%H:%M, %d/%m, %Y', time.localtime())}. Provide this information in a conversational way if requested, for example: its 23 minutes past 9, or: its almost quarter to 7. Only provide the day, month, or year if specifically asked to.")

        # initialises api client
        self.__client = OpenAI(api_key=API_KEY)

        self.__speech_file_path = "Speech\\speech.mp3"

    @staticmethod
    def completion_message(role: str, content: str) -> dict[str, str]:
        return {
            "role": role,
            "content": content
        }

    def get_new_status(self) -> str:
        """
        Makes a request to the api for a new custom status
        :return: the new status as a string
        """
        input_message = self.completion_message("user", STATUS_PROMPT)
        return self.make_chat_request(input_message)

    def wakeup_message(self) -> (str, str):
        """
        Makes a new request to the api for a 'greeting' to send when the discord client is activated
        :return: the message as a string
        """
        input_message = self.completion_message("developer", WAKEUP_PROMPT)
        return self.make_chat_request(input_message)

    def make_chat_request(self, input_message: dict[str, str] | None = None,input_messages: list[dict[str, str]] | None = None) -> str | None:
        """
        makes a request to the openai api

        should have either input or inputs, inputs is prioritised

        :param input_message: single message to send
        :param input_messages: list containing messages to send
        :return: Returns the completion message as a string
        """

        if input_messages:
            message_list = [self.__system_message] + input_messages + [self.__time_message]
        elif input_message:
            message_list = [self.__system_message, input_message, self.__time_message]
        else:
            return

        # uses gpt-4o-mini for text completions
        completion = self.__client.chat.completions.create(
            model="gpt-4o-mini",
            messages=message_list,
            frequency_penalty=2,
            max_completion_tokens=64
        )
        self.__amy_logger.log_token_usage(completion.usage.prompt_tokens, completion.usage.completion_tokens)
        return completion.choices[0].message.content

    def make_voice_request(self, input: str) -> str:
        response = self.__client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=input
        )
        response.stream_to_file(self.__speech_file_path)
        return self.__speech_file_path
