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

def delete_member_data(discord_id, discord_name):
    try:
        db.member_data.delete_one({"discord_id": discord_id})
    except Exception as e:
        print(f"error: {e}")
    else:
        print(f"{discord_name} 님이 서버를 탈퇴하셨습니다.")

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
        delete_member_data(member.id, str(member))




async def setup(bot):
    await bot.add_cog(Listener(bot), guilds=[discord.Object(id=GUILD_ID)])