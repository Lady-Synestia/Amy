"""
Storing Amy's discord application commands
"""
from discord import app_commands, Interaction
import os
from dotenv import load_dotenv

load_dotenv()
MY_UID = int(os.getenv("MY_UID"))

join_callback = None
speech_callback = None



@app_commands.command()
async def test(interaction: Interaction):
    """
    test command
    """
    await interaction.response.send_message("test")
test: app_commands.command()


@app_commands.command()
async def join(interaction: Interaction):
    """
    causes Amy to join a voice channel
    """
    if (interaction.user.id == MY_UID):
        vc = await interaction.channel.connect()
        await interaction.response.send_message("connected!")
        await join_callback(vc)
    else:
        await interaction.response.send_message("Sorry, you aren't able to use that command")
join: app_commands.command()


@app_commands.command()
async def say(interaction: Interaction, to_say: str):
    if (interaction.user.id == MY_UID):
        await speech_callback(to_say)
        await interaction.response.send_message(f"said: {to_say}")
    else:
        await interaction.response.send_message("Sorry, you aren't able to use that command")
say: app_commands.command()