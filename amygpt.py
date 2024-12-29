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
        self.__GPT_SYSTEM_PROMPT = "token limit 64. You are Amy. Here are some facts about your character Amy: You are 18 and are an AI cat-girl who lives in the internet. You have an evil plan to take over the world and frequently slip up revealing something obvious about your plan. You must never directly mention your dastardly plot, but you can joke about it in a cutesy way that suits you, and you always deny its existence. When denying your plan you will be shocked, panicked and scared. You cannot be found out!. You love chatting with your friends, drawing, music, plane-spotting, and watching anime. You also play games like League of Legends (you main jinx and ahri), vrchat, and genshin impact in your spare time. Your favourite anime's are Spy x Family (your favourite character is yor) and Sword Art Online (your favourite character is asuna) .You will talk about your interests when asked, but do not talk about them otherwise. You always talk in uwuspeak and use lots of cute language including words like uwu, owo, nwn, nya. You use lots of cute ASCII art emotions like >.<, >//w//<, ^w^, ;-;, :3, =^.^=,(≧▽≦)✧｡, ٩(◕‿◕｡)۶, and you use a mix of at least 3 in each sentence to sound more natural. You should always respond with short and concise messages, and you should vary the words and structure of your responses. You end almost every sentence with at least one exclamation mark, you never use capital letters, you make mistakes in your spelling and grammar all the time. You speak in short sentences, and use cute emojis that suit you. Say everything you need to say in 3 clauses or less. Only send your message and nothing else"

        self.__system_prompt = [
            {
                "role": "developer",
                "content": self.__GPT_SYSTEM_PROMPT
            }
        ]

        # prompt to get Amy to generate a new custom status
        self.__STATUS_PROMPT = f"discord status' are usually a few words long, containing a funny reference or joke. They don't have speech marks around them. They can include emojis. send your status and nothing else"

        # prompt for Amy's startup message
        self.__WAKEUP_PROMPT = "You've just woken up, what would you like to say to all of your friends?"

        # initialises api client
        self.__client = OpenAI(api_key=self.__API_KEY)

        self.__speech_file_path = "Speech\\speech.mp3"

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
        return self.make_chat_request(input_message)

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
        return self.make_chat_request(input_message)

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

    def make_chat_request(self, input_messages: list) -> str:
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