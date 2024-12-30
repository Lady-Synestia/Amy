"""
Handling Amy's GPT-4o-mini completions
"""

from openai import OpenAI
from amylogging import log_token_usage
from amyconfig import open_ai_configs as configs


class AmyGPT:
    def __init__(self):
        self.__system_message = self.completion_message("developer", configs.system_prompt)

        self.__weight_message = self.completion_message("developer", configs.weight_prompt)

        # initialises api client
        self.__client = OpenAI(api_key=configs.api_key)

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
        input_messages = [self.completion_message("user", configs.status_prompt)]
        return self.make_chat_request(input_messages)

    def wakeup_message(self) -> (str, str):
        """
        Makes a new request to the api for a 'greeting' to send when the discord client is activated
        :return: the message as a string
        """
        input_messages = [self.completion_message("developer", configs.wakeup_prompt)]
        return self.make_chat_request(input_messages)

    def make_weight_request(self, message: str) -> float:
        """
        Makes a request to the api for a weight, used to determine how likely Amy is to reply to a message
        :return: the weight as a float
        """
        message_list = [self.__weight_message, self.completion_message("user", message)]

        completion = self.__client.chat.completions.create(
            model="gpt-4o-mini",
            messages=message_list,
            temperature=0.5
        )
        log_token_usage(completion.usage.prompt_tokens, completion.usage.completion_tokens)
        return float(completion.choices[0].message.content)

    def make_chat_request(self, input_messages: list[dict[str, str]]) -> str | None:
        """
        makes a request to the openai api

        should have either input or inputs, inputs is prioritised

        :param input_messages: tuple containing messages to send
        :return: Returns the completion message as a string
        """
        if len(input_messages) == 0:
            return

        # time_message = self.completion_message("developer", prompts.time)
        message_list = [self.__system_message] + input_messages

        # uses gpt-4o-mini for text completions
        completion = self.__client.chat.completions.create(
            model="gpt-4o-mini",
            messages=message_list,
            frequency_penalty=2,
            max_completion_tokens=64
        )
        log_token_usage(completion.usage.prompt_tokens, completion.usage.completion_tokens)
        return completion.choices[0].message.content

    def make_voice_request(self, to_say: str) -> str:
        """
        Makes a text-to-speech request to the voice api
        :param to_say: text to send
        :return: file path of the voice response
        """
        response = self.__client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=to_say
        )
        response.stream_to_file(self.__speech_file_path)
        return self.__speech_file_path
