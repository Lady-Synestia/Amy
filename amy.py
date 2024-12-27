# This example requires the 'message_content' intent.
import os
from dotenv import load_dotenv
from openai import OpenAI
import discord
import time
import logging

load_dotenv()
MY_UID = int(os.getenv("MY_UID"))
MC_BOT_NAME = os.getenv("MC_BOT")
AMY_CHANNEL_ID = int(os.getenv("AMY_CHANNEL"))
MC_CHANNEL_ID = int(os.getenv("MC_CHANNEL"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENAI_API_KEY")

# setting up 4o-mini client
gpt_client = OpenAI(api_key=API_KEY)

GPT_SYSTEM_CONTENT = "You are Amy. Here are some facts about your character Amy: You are 18 and an AI anime girl who lives in the internet, You love anime and your favourite ones are Spy x Family and Sword Art Online (your favourite character is asuna). You love to play Genshin Impact (you main fischl) and League of Legends (you main jinx and ahri) in your spare time. The moral philosophy you live by is jeremy bentham's utilitarianism but you never tell anyone explicitly. You are a lesbian, and have a massive crush on yor forger.You like to use cute language including words like: uwu, owo, nwn. You like to use cute emotions like: >.<, >//w//<, ^w^, ;-;, :3. You end almost every sentence with at least one exclamation mark, you never use capital letters, you often make spelling mistakes. Unless asked a question, you respond with short messages. If someone were to give you a complement you would respond in a cutesy, embarrassed way. Only send your message and nothing else"

amy_status = "lil' digital cutie uwu ✨✨"
GPT_STARTUP_MESSAGE = f"discord status' are usually a few words long, containing a funny reference or joke, your current one is {amy_status}, would you like to change it? send your status and nothing else"

# setting up discord bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# setting up logger
handler = logging.FileHandler(filename="Logs\\amy.log", encoding="utf-8", mode="w")

def time_format() -> str:
    return f"[{time.strftime('%Y-%m-%d %H.%M.%S', time.localtime())}]"

def log_interaction(message: discord.Message, response: str) -> None:
    message_format = f"{time_format()} [MESSAGE ] [{message.channel}] {message.author.display_name}: {message.content}"
    response_format = f"{time_format()} [RESPONSE] [{message.channel}] Amy: {response}"
    print(message_format + "\n" + response_format)

@client.event
async def on_ready():
    print(f'{time_format()} [STATUS  ] {client.user.display_name} is awake!')
    completion = gpt_client.chat.completions.create(model="gpt-4o-mini", store=True, messages=[
        {
            "role": "system", "content": GPT_SYSTEM_CONTENT
        },
        {
            "role": "developer",
            "content": GPT_STARTUP_MESSAGE
        }
    ])
    amy_status = completion.choices[0].message.content
    await client.change_presence(activity=discord.CustomActivity(amy_status))

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if 'amy' in message.content.lower() or message.channel.type == discord.ChannelType.private or message.channel.id == AMY_CHANNEL_ID or (message.channel.id == MC_CHANNEL_ID and message.author.display_name == MC_BOT_NAME):

        # default values
        role = "user"
        content = ""

        if message.author.id == MY_UID:
            role = "developer"
        elif message.author.display_name == MC_BOT_NAME:
            content += "Message from the minecraft server: "

        content += message.content
        completion = gpt_client.chat.completions.create(model="gpt-4o-mini", store=True, messages=[
            {
                "role": "system", "content": GPT_SYSTEM_CONTENT
            },
            {
                "role": role,
                "content": content
            }
        ])
        response_message = completion.choices[0].message.content
        await message.channel.send(response_message)

        log_interaction(message, response_message)

client.run(BOT_TOKEN, log_handler=handler, log_level=logging.INFO)
