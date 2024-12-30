"""
Storing Amy's discord application commands
"""
import discord
from discord import app_commands, Interaction
from typing import Callable
from amyconfig import discord_configs as configs
from amylogging import log_command


class UnAuthorizedUserException(Exception):
    pass


async def respond(interaction: Interaction, response: str) -> None:
    """
    Responds to a command
    wraps discord.InteractionResponse.respond, using common default values
    :param interaction: discord Interaction
    """
    await interaction.response.send_message(response, ephemeral=True)


async def auth_check(interaction: Interaction) -> bool:
    """
    checks user id against authorised users
    :param interaction: discord interaction
    :return: true if user is authorised
    """
    try:
        if interaction.user.id in configs.authorised_users:
            return True
        else:
            raise UnAuthorizedUserException
    except UnAuthorizedUserException:
        await respond(interaction, "Sorry, you aren't able to use that command")
        return False


join: app_commands.command()
join_callback: Callable


@app_commands.command(description="Causes Amy to join a a voice channel")
async def join(interaction: Interaction) -> None:
    """
    causes Amy to join a voice channel
    """
    if await auth_check(interaction) and interaction.channel.type == discord.ChannelType.voice:
        log_command(interaction, "join")
        vc = await interaction.channel.connect()
        await respond(interaction, "connected!")
        if join_callback is not None:
            await join_callback(vc)


leave: app_commands.command()
leave_callback: Callable


@app_commands.command(description="Causes Amy to leave a voice channel")
async def leave(interaction: Interaction) -> None:
    """
    causes Amy to leave a voice channel
    """
    if await auth_check(interaction):
        log_command(interaction, "leave")
        if leave_callback is not None:
            await leave_callback()
            await respond(interaction, "leaving!")


say: app_commands.command()
say_callback: Callable


@app_commands.command(description="Causes Amy to speak a voice message")
async def say(interaction: Interaction, to_say: str) -> None:
    """
    Causes Amy to say a voice message
    :param to_say: text to convert to audio
    """
    if await auth_check(interaction):
        log_command(interaction, "say", to_say)
        if say_callback is not None:
            await say_callback(to_say)
            await respond(interaction, f"said: {to_say}")


echo: app_commands.command()
echo_callback: Callable


@app_commands.command(description="Causes Amy to send a custom message")
async def echo(interaction: Interaction, content: str) -> None:
    """
    Causes Amy to echo a message
    :param content: content of the message
    """
    if await auth_check(interaction):
        log_command(interaction, "echo", content)
        if echo_callback is not None:
            await echo_callback(interaction.channel, content)
            await respond(interaction, f"echoed: {content}")


activity: app_commands.command()
activity_callback: Callable


@app_commands.command(description="Causes Amy to display a custom activity, or update her current one")
async def activity(interaction: Interaction, custom: str = None) -> None:
    """
    Causes Amy to display a custom activity, or update her current one
    :param custom: her new activity - she generates her own if this is none
    """
    if await auth_check(interaction):
        log_command(interaction, "activity", custom)
        if activity_callback is not None:
            await activity_callback(custom)
            await respond(interaction, f"updated activity!")


r: app_commands.command()
r_callback: Callable


@app_commands.command(description="Changes Amy's response threshold")
async def r(interaction: Interaction, value: float | None) -> None:
    """
    Changes Amy's response threshold, resets it if no value is given
    :param value: value to set R to, float between -1 and 1
    """
    if await auth_check(interaction):
        log_command(interaction, "R", value)
        if r_callback is not None:
            value = r_callback(value)
            await respond(interaction, f"Updated response threshold: {value}")
