import os
from dotenv import load_dotenv
import pymongo
import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get


load_dotenv(".env")
MONGO_URL = os.getenv('MONGO_URL')
GUILD_ID = os.getenv('GUILD_ID')

mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client.member
last_member_data = None





class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Test Cog loaded")

    @app_commands.command(name="테스트", description="테스트")
    async def information(self, interaction: discord.Interaction):
        roles = interaction.user.roles
        print(roles)
        for role in roles:
            if(str(role) == "@everyone"):
                pass
            else:
                await interaction.user.remove_roles(get(interaction.user.roles, name=str(role)))
        await interaction.response.send_message(f"{interaction.user.roles}", ephemeral=True)




async def setup(bot):
    await bot.add_cog(Test(bot), guilds=[discord.Object(id=GUILD_ID)])