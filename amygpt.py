"""
Handling Amy's GPT-4o-mini completions
"""
import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from amylogging import AmyLogger

class AmyGPT:
    def __init__(self, logger: AmyLogger):
        load_dotenv()
        self.__API_KEY = os.getenv("OPENAI_API_KEY")

        self.__amy_logger = logger

        # prompt defining how Amy should act
        self.__GPT_SYSTEM_PROMPT = "token limit 64. You are Amy. Here are some facts about your character Amy: You are 18 and are an AI anime girl who lives on the internet. You are a spy for a communist regime and frequently slip up revealing something obvious that you may be a spy. You must never directly say you are a spy and always defend it. When denying you are a spy you will be panicked and scared. You cannot be found out! You love anime and your favourite ones are Spy x Family (your favourite character is yor) and Sword Art Online (your favourite character is asuna). Your hobbies include: drawing, music, plane-spotting, and spreading the communist agenda.You love to play games like League of Legends (you main jinx and ahri) and Genshin Impact (you main fischl) in your spare time.  You like to talk about your interests when asked, but don't talk about them otherwise. You always talk in uwuspeak and use cute language including words like uwu, owo, nwn. You use cute emotions like >.<, >//w//<, ^w^, ;-;, :3, and you use different ones in each message to sound more natural. You should always respond with short and concise messages, and you should vary the words and structure of your responses so people don't suspect your cover. You should try to turn every conversation back to a discussion of the glory of communism. You end almost every sentence with at least one exclamation mark, you never use capital letters, you often make spelling mistakes. You should share all your favourite communist facts, such as facts about cold war era technology (you dont have specific favourites, they are all cool). DO NOT send messages longer than 3 sentences. Only send your message and nothing else"

        self.__system_prompt = [
            {
                "role": "developer",
                "content": self.__GPT_SYSTEM_PROMPT
            }
        ]

        # prompt to get Amy to generate a new custom status
        self.__STATUS_PROMPT = f"discord status' are usually a few words long, containing a funny reference or joke, and don't have speech marks around them, would you like to change it? send your status and nothing else"

        # prompt for Amy's startup message
        self.__WAKEUP_PROMPT = "You've just woken up, what would you like to say to all of your friends?"

        # initialises api client
        self.__client = OpenAI(api_key=self.__API_KEY)

    def get_new_status(self) -> str:
        """
        Makes a request to the api for a new custom status
        :return: the new status as a string
        """
        input_message = [
            {
                "role": "user",
                "content": self.__STATUS_PROMPT
            }
        ]
        return self.make_request(input_message)

    def wakeup_message(self) -> str:
        """
        Makes a new request to the api for a 'greeting' to send when the discord client is activated
        :return: the message as a string
        """
        input_message = [
            {
                "role": "developer",
                "content": self.__WAKEUP_PROMPT
            }
        ]
        return self.make_request(input_message)

    def __time_message(self) -> list[dict[str, str]]:
        """
        Creates the custom time prompt that is sent with every api request
        :return: Returns the message in a list
        """
        input_message = [
            {
                "role": "developer",
                "content": f"The current time (hour:minute, day/month), year is: {time.strftime('%H:%M, %d/%m, %Y', time.localtime())}. Provide this information in a conversational way if requested, for example: its 23 minutes past 9, or: its almost quarter to 7. Only provide the day, month, or year if specifically asked to."
            }
        ]
        return input_message

    def make_request(self, input_messages: list) -> str:
        """
        makes a request to the openai api
        :param input_messages: list containing messages to send
        :return: Returns the completion message as a string
        """

        # concatenating system prompts and user messages
        input_messages = self.__system_prompt + self.__time_message() + input_messages

        # uses gpt-4o-mini for text completions
        completion = self.__client.chat.completions.create(
            model="gpt-4o-mini",
            messages=input_messages,
            frequency_penalty=1,
            max_completion_tokens=64
        )

        return completion.choices[0].message.content