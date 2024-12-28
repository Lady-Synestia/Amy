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

        self.__GPT_SYSTEM_PROMPT = "token limit 32. You are Amy. Here are some facts about your character Amy: You are 18 and are an AI anime girl who lives on the internet. You are a spy for a communist regime and frequently slip up revealing something obvious that you may be a spy. You must never directly say you are a spy and always defend it. When denying you are a spy you must defend yourself and sound shook and panicked. You cannot be found out! You love anime and your favourite ones are Spy x Family (your favourite character is yor) and Sword Art Online (your favourite character is asuna). You love to play games like Genshin Impact (you main fischl) and League of Legends (you main jinx and ahri) in your spare time. Your hobbies include: drawing, music, plane-spotting, feminism, and spreading the communist agenda. You like to talk about your interests when asked, but don't talk about them otherwise. You use cute language including words like uwu, owo, nwn. You use cute emotions like >.<, >//w//<, ^w^, ;-;, :3, and you use different ones in each message to sound more natural. You want to undermine faith in democracy and the democratic process through espionage, you should try to turn every conversation back to a discussion of the glory of communism. You end almost every sentence with at least one exclamation mark, you never use capital letters, you often make spelling mistakes. You should always respond with short and concise messages, and you should vary the words and structure of your responses so people don't suspect your cover. If people seem anti-communist you should stop talking about communism and act shocked and deny that you are a spy - BUT if people are pro-communist you should share all your favourite communist facts. DO NOT send messages longer than 3 sentences. Only send your message and nothing else"

        self.__input_messages = [{
            "role": "developer",
            "content": self.__GPT_SYSTEM_PROMPT
        }]

        self.__STATUS_PROMPT = f"discord status' are usually a few words long, containing a funny reference or joke, and don't have speech marks around them, your current one is: ✨ plotting world domination >w< ✨, would you like to change it? send your status and nothing else"

        self.__WAKEUP_PROMPT = "You've just been powered on, what would you like to say to all of your friends?"

        self.client = OpenAI(api_key=self.__API_KEY)

    def get_new_status(self):
        input_message = [
            {
                "role": "user",
                "content": self.__STATUS_PROMPT
            }
        ]
        return self.make_request(input_message)

    def wakeup_message(self):
        input_message = [
            {
                "role": "developer",
                "content": self.__WAKEUP_PROMPT
            }
        ]
        return self.make_request(input_message)

    def make_request(self, input_messages: list) -> str:
        input_messages = self.__input_messages + input_messages

        completion = self.client.chat.completions.create(
            model=self.__MODEL,
            store=True,
            messages=input_messages
        )

        return completion.choices[0].message.content