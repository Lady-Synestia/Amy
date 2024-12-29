"""
Storing Amy's discord application commands
"""
import discord
from discord import app_commands, Interaction
from typing import Callable
from amyconfig import permissions


@app_commands.command()
async def join(interaction: Interaction):
    """
    causes Amy to join a voice channel
    """
    if interaction.user.id == permissions.users[0]:
        vc = await interaction.channel.connect()
        await interaction.response.send_message("connected!")
        if join_callback is not None:
            await join_callback(vc)
    else:
        await interaction.response.send_message("Sorry, you aren't able to use that command")


join: app_commands.command()
join_callback: Callable


@app_commands.command()
async def leave(interaction: Interaction):
    """
    causes Amy to leave a voice channel
    """
    if interaction.user.id == permissions.users[0]:
        if leave_callback is not None:
            await leave_callback()
            await interaction.response.send_message("left!")
    else:
        await interaction.response.send_message("Sorry, you aren't able to use that command")


leave: app_commands.command()
leave_callback: Callable


@app_commands.command()
async def say(interaction: Interaction, to_say: str):
    if interaction.user.id == permissions.users[0]:
        if say_callback is not None:
            await say_callback(to_say)
            await interaction.response.send_message(f"said: {to_say}")
    else:
        await interaction.response.send_message("Sorry, you aren't able to use that command")


say: app_commands.command()
say_callback: Callable
