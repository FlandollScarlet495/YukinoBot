import discord
from discord import app_commands
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="挨拶します")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"こんにちは、{interaction.user.mention} さん！🌸")

async def setup(bot):
    await bot.add_cog(Example(bot))
