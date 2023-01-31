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


class Attendance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Attendance Cog loaded")

    @commands.command(name="출석")
    async def attendance(self, ctx):
        if(ctx.author == ctx.guild.owner):
            await ctx.send(ctx.channel)
            await ctx.send(str(ctx.channel) == "봇테스트")
            await ctx.send(ctx.channel=="봇테스트")
            await ctx.send(ctx.channel.members)
            for member in ctx.channel.members:
                await ctx.send(member.name)
            await ctx.send("출석체크 완료")
        else:
            await ctx.send("선생님만 출석체크가 가능합니다.")




async def setup(bot):
    await bot.add_cog(Attendance(bot), guilds=[discord.Object(id=GUILD_ID)])