import os
from dotenv import load_dotenv
import pymongo
import discord
from discord import app_commands
from discord.ext import commands

load_dotenv(".env")
MONGO_URL = os.getenv('MONGO_URL')
GUILD_ID = os.getenv('GUILD_ID')

mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client.member
last_member_data = None


def give_coin(key:dict):
    db.member_data.update_one(key, {"$inc": {"r_coin": 100}}, True)

def is_owner(interaction: discord.Interaction):
    return interaction.user == interaction.guild.owner
def is_class(interaction: discord.Interaction):
    return "교시" in str(interaction.channel)

class Attendance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Attendance Cog loaded")

    @app_commands.command(name="출석", description="수업시간 출석체크 기능. (알코인 지급)")
    @app_commands.check(is_owner)
    @app_commands.check(is_class)
    async def attendance(self, interaction: discord.Interaction):
        for member in interaction.channel.members:
            try:
                give_coin({"discord_id": member.id})
            except Exception as e:
                await interaction.response.send_message(f"오류로 인해 {member.name} 님의 알코인은 적립되지 않았습니다.")
                print(e)
            else:
                await interaction.response.send_message(f"{member.name} 님에게 100 알코인이 적립되었습니다.")
        await interaction.send("출석체크 완료")

    @attendance.error
    async def attendance_error(self, interaction: discord.Interaction, error):
        if not is_owner(interaction):
            await interaction.response.send_message("선생님만 출석체크가 가능합니다.", ephemeral=True)
        elif not is_class(interaction):
            await interaction.response.send_message("수업 채널에서만 출석체크가 가능합니다.", ephemeral=True)
        





async def setup(bot):
    await bot.add_cog(Attendance(bot), guilds=[discord.Object(id=GUILD_ID)])