"""
Storing Amy's discord application commands
"""
from discord import app_commands, Interaction


@app_commands.command()
async def test(interaction: Interaction):
    await interaction.response.send_message("test")
test: app_commands.command()