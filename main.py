import pandas as pd
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv(".env")
BOT_TOKEN = os.getenv('BOT_TOKEN')



intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents, application_id="1064890345634152510")

@bot.event
async def on_ready():
    #Cog 불러오기
    for f in os.listdir("./Cogs"):
        if f.endswith(".py"):
            await bot.load_extension("Cogs." + f[:-3])
    print(f'{bot.user} 로그인 완료')


@bot.command(name="clear")
async def clear(ctx, *count):
    if(ctx.author == ctx.guild.owner):
        try:
            await ctx.channel.purge(limit=99999 if (len(count)==0) or (int(count[0])==0) else int(count[0])+1)
        except:
            await ctx.send(f'명령문 오류입니다. 다시 입력해주세요.\n $clear 개수(숫자)')
            await ctx.channel.delete_messages([ctx.message])


bot.run(BOT_TOKEN)