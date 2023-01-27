import os
from dotenv import load_dotenv
import pymongo
import discord
from discord.ext import commands
from discord import app_commands
import asyncio

load_dotenv(".env")
BOT_TOKEN = os.getenv('BOT_TOKEN')
MONGO_URL = os.getenv('MONGO_URL')
APP_ID = os.getenv('APP_ID')


client = pymongo.MongoClient(MONGO_URL)
db = client.test


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all(),
            sync_command=True,
            application_id=APP_ID
        )
        print("MyBot init!")
    async def setup_hook(self) -> None:
        #Cog 불러오기
        for f in os.listdir("./Cogs"):
            if f.endswith(".py"):
                await self.load_extension("Cogs." + f[:-3])
        await self.tree.sync(guild=discord.Object(id=1060440200192475206))
        print("slash command synced!")

bot = MyBot()

@bot.command(name="clear")
async def clear(ctx, *count):
    if(ctx.author == ctx.guild.owner):
        try:
            await ctx.channel.purge(limit=99999 if (len(count)==0) or (int(count[0])==0) else int(count[0])+1)
        except:
            await ctx.send(f'명령문 오류입니다. 다시 입력해주세요.\n $clear 개수(숫자)')
            await ctx.channel.delete_messages([ctx.message])


        
bot.run(BOT_TOKEN)
