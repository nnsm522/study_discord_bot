import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import db_module

load_dotenv(".env")
MONGO_URL = os.getenv('MONGO_URL')
GUILD_ID = os.getenv('GUILD_ID')


class Listener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Listener Cog loaded")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if "정보인증" in str(message.channel):    
            if message.author.bot:
                pass
            else:
                await message.delete()
                await message.channel.send('정보인증만 가능한 채널입니다.\n"/" 입력 후 [/정보]를 선택하여 정보를 등록해주세요.')
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await db_module.delete_member_data(member.id)
        print(f"{str(member)} 서버 탈퇴")



async def setup(bot):
    await bot.add_cog(Listener(bot), guilds=[discord.Object(id=GUILD_ID)])