import pandas as pd
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv(".env")
BOT_TOKEN = os.getenv('BOT_TOKEN')


def csv_id(id):
    return f"'{id}"

def command_error_message(command_name):
    return (f'잘못 입력하셨습니다. {command_name} 명령어는 아래와 같이 입력해주세요.\n')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    #Cog 불러오기
    for f in os.listdir("./Cogs"):
        if f.endswith(".py"):
            await bot.load_extension("Cogs." + f[:-3])
    print(f'{bot.user} 로그인 완료')

#테스트용
@bot.command()
async def test(ctx, *args):
    await ctx.send(f'\
type(ctx.guild) : {type(ctx.guild)}\nctx.guild : {ctx.guild}\n\
type(ctx.channel) : {type(ctx.channel)}\nctx.channel : {ctx.channel}\n\
type(ctx.author) : {type(ctx.author)}\nctx.author : {ctx.author}\n\
type(ctx.channel.members) : {type(ctx.channel.members)}\nctx.channel.members : {ctx.channel.members}\n\
')

'''
@bot.command(name="멤버보기")
async def student_find_all(ctx):
    async for member in ctx.guild.fetch_members(limit=150):
        await ctx.send(member)

@bot.command(name="입금확인")
async def deposit_check(ctx):
    #오픈뱅킹 API 이용하여 거래내역 확인 후 역할조정
    await ctx.send("deposit_check")
'''

@bot.command(name="clear")
async def clear(ctx, *count):
    if(ctx.author == ctx.guild.owner):
        try:
            await ctx.channel.purge(limit=99999 if (len(count)==0) or (int(count[0])==0) else int(count[0])+1)
        except:
            await ctx.send(f'명령문 오류입니다. 다시 입력해주세요.\n $clear 개수(숫자)')
            await ctx.channel.delete_messages([ctx.message])


bot.run(BOT_TOKEN)