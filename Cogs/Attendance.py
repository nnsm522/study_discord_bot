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

def is_owner(ctx):
    return ctx.author == ctx.guild.owner
def is_class(ctx):
    return str(ctx.channel) == "수업"

class Attendance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Attendance Cog loaded")

    @commands.command(name="출석")
    @commands.check(is_owner)
    @commands.check(is_class)
    async def attendance(self, ctx):
        for member in ctx.channel.members:
            try:
                give_coin({"discord_id": member.id})
            except Exception as e:
                await ctx.send(f"오류로 인해 {member.name} 님의 알코인은 적립되지 않았습니다.")
                print(e)
            else:
                await ctx.send(f"{member.name} 님에게 100 알코인이 적립되었습니다.")
        await ctx.send("출석체크 완료")

    @attendance.error
    async def attendance_error(self, ctx, error):
        if not is_owner(ctx):
            await ctx.send("선생님만 출석체크가 가능합니다.")
        elif not is_class(ctx):
            await ctx.send("수업 채널에서만 출석체크가 가능합니다.")
        





async def setup(bot):
    await bot.add_cog(Attendance(bot), guilds=[discord.Object(id=GUILD_ID)])