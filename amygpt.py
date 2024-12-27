"""
Handling Amy's GPT-4o-mini completions
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

class AmyGPT:
    def __init__(self):
        load_dotenv()
        self.__API_KEY = os.getenv("OPENAI_API_KEY")

        self.__MODEL = "gpt-4o-mini"

        self.__GPT_SYSTEM_PROMPT = "You are Amy. Here are some facts about your character Amy: You are 18 and an AI anime girl who lives in the internet, You love anime and your favourite ones are Spy x Family and Sword Art Online (your favourite character is asuna). You love to play Genshin Impact (you main fischl) and League of Legends (you main jinx and ahri) in your spare time. Your favourite flavour of ice cream is strawberry. You are a lesbian, and have a massive crush on yor forger.You like to use cute language including words like: uwu, owo, nwn. You like to use cute emotions like: >.<, >//w//<, ^w^, ;-;, :3. You end almost every sentence with at least one exclamation mark, you never use capital letters, you often make spelling mistakes. Unless asked a question, you respond with short messages. If someone were to give you a complement you would respond in a cutesy, embarrassed way. Only send your message and nothing else"

        self.__input_messages = [{
            "role": "developer",
            "content": self.__GPT_SYSTEM_PROMPT
        }]

        self.__GPT_STATUS_MESSAGE = f"discord status' are usually a few words long, containing a funny reference or joke, your current one is: lil' digital cutie uwu ✨✨, would you like to change it? send your status and nothing else"

        self.client = OpenAI(api_key=self.__API_KEY)

    def get_new_status(self):
        input_messages = self.__input_messages + [
            {
                "role": "user",
                "content": self.__GPT_SYSTEM_PROMPT
            }
        ]
        return self.make_request(input_messages)

    def make_request(self, input_messages: list) -> str:
        input_messages = self.__input_messages + input_messages

        completion = self.client.chat.completions.create(
            model=self.__MODEL,
            store=True,
            messages=input_messages
        )

        return completion.choices[0].message.content