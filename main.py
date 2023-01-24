import pandas as pd
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv(".env")
BOT_TOKEN = os.getenv('BOT_TOKEN')

t_num = 0

# #학생 정보 csv 파일 불러오기
# student_info_path = "./data/student_info.csv"
# student_info = pd.read_csv(student_info_path)
# student_info.set_index('discord id', inplace=True)

# #시험 성적 csv 파일 불러오기
# exam_grades_path = "./data/exam_grades.csv"
# exam_grades = pd.read_csv(exam_grades_path)
# exam_grades.set_index('discord id', inplace=True)

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
@bot.command(name="정보_입력")
async def score_reset(ctx, *args):
    if(len(args) == 4):
        student_info.loc[csv_id(ctx.author.id)] = [str(ctx.author), args[0], args[1], args[2], args[3]]
        student_info.to_csv(student_info_path, encoding='utf-8-sig')
        if(csv_id(ctx.author.id) in exam_grades.index.tolist()):
            pass
        else:
            exam_grades.loc[csv_id(ctx.author.id)] = [None,None,None,None,None,None,None,None,None,None,None,None]
            exam_grades.to_csv(exam_grades_path, encoding='utf-8-sig')
        await ctx.send(f'{ctx.author}님이 등록되었습니다.\n{student_info.loc[csv_id(ctx.author.id)]}')
    else:
        await ctx.send(f'{command_error_message("정보_입력")}\
$정보\_입력 [이름] [생년월일] [학교] [연락처]\n\
예시) $정보\_입력 홍길동 100522 한국중학교 010-1234-5678')

@bot.command(name="정보_확인")
async def score_reset(ctx):
    await ctx.send(f'{ctx.author}님의 정보입니다.\n\n{student_info.loc[csv_id(ctx.author.id)]}\n\n\
명령어를 통해 정보를 수정할 수 있습니다.\n\U0001F449 $정보\_입력 [이름] [생년월일] [학교] [연락처]')

@bot.command(name="시험성적_확인")
async def score_reset(ctx):
    await ctx.send(f'{ctx.author}님의 시험성적입니다.\n\n{exam_grades.loc[csv_id(ctx.author.id)]}\n\n\
명령어를 통해 정보를 수정할 수 있습니다.\n\U0001F449 $시험성적\_입력 [어떤시험] [점수]')

@bot.command(name="시험성적_입력")
async def score_reset(ctx, *args):
    if(args[0] in exam_grades.columns.values.tolist()):
        try:
            exam_grades.loc[csv_id(ctx.author.id), args[0]] = int(args[1])
            exam_grades.to_csv(exam_grades_path, encoding='utf-8-sig')
            await ctx.send(f'{ctx.author}님의 성적이 등록되었습니다.\n{exam_grades.loc[csv_id(ctx.author.id)]}')
        except:
            await ctx.send(f'{command_error_message("시험성적_입력")}\
$시험성적_입력 [어떤시험] [점수] \n\
예시) $시험성적\_입력 2-1중간 90\n\
\U00002757 점수는 숫자로만 입력하세요. \U00002757')
    else:
        await ctx.send(f'{command_error_message("시험성적_입력")}\
$시험성적_입력 [어떤시험] [점수] \n\
예시) $시험성적\_입력 2-1중간 90\n\
시험목록 : {exam_grades.columns.values.tolist()}')



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