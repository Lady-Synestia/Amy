"""
Storing Amy's discord application commands
"""
from discord import app_commands, Interaction

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
    vc = await interaction.channel.connect()
    await join_callback(vc)
    await interaction.response.send_message("connected!")
join: app_commands.command()


@app_commands.command()
async def say(interaction: Interaction, to_say: str):
    await speech_callback(to_say)
    await interaction.response.send_message(f"said: {to_say}")
say: app_commands.command()