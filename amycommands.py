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
        await interaction.response.send_message("connected!", ephemeral=True)
        if join_callback is not None:
            await join_callback(vc)
    else:
        await interaction.response.send_message("Sorry, you aren't able to use that command", ephemeral=True)


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
            await interaction.response.send_message("left!", ephemeral=True)
    else:
        await interaction.response.send_message("Sorry, you aren't able to use that command", ephemeral=True)


leave: app_commands.command()
leave_callback: Callable


@app_commands.command()
async def say(interaction: Interaction, to_say: str):
    if interaction.user.id == permissions.users[0]:
        if say_callback is not None:
            await say_callback(to_say)
            await interaction.response.send_message(f"said: {to_say}", ephemeral=True)
    else:
        await interaction.response.send_message("Sorry, you aren't able to use that command", ephemeral=True)


say: app_commands.command()
say_callback: Callable


@app_commands.command()
async def echo(interaction: Interaction, content: str):
    if interaction.user.id == permissions.users[0]:
        if echo_callback is not None:
            await echo_callback(interaction.channel, content)
            await interaction.response.send_message(f"echoed: {content}", ephemeral=True)
    else:
        await interaction.response.send_message("Sorry, you aren't able to use that command", ephemeral=True)

echo: app_commands.command()
echo_callback: Callable
