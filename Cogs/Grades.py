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
selected_grade = "중1"


#command 호출한 사람의 데이터 불러와서 저장
def import_member_data(discord_id):
    global last_member_data
    last_member_data = db.member_data.find_one({"discord_id": discord_id})
   
#DB 재호출
def call_DB():
    global db
    db = mongo_client.member

def update_member_data(discord_id, exam_grades):
    global db
    key = {"discord_id": discord_id}
    data = {"성적": exam_grades}
    try:
        db.member_data.update_one(key, {"$set": data}, True)
    except Exception as e:
        print(f"error: {e}")
    else:
        call_DB()
        print("DB update Success!")

#t성적 입력/수정 시 Modal창에 기본으로 입력되어있을 값 수정
def default_data_setting(last_member_data, grade):
    if last_member_data is not None:
        InputGradesModal.grade = grade
        InputGradesModal.grades1.label = f"{grade}-1중간"
        InputGradesModal.grades2.label = f"{grade}-1기말"
        InputGradesModal.grades3.label = f"{grade}-2중간"
        InputGradesModal.grades4.label = f"{grade}-2기말"
        InputGradesModal.grades1.default = last_member_data["성적"][f"{grade}-1중간"]
        InputGradesModal.grades2.default = last_member_data["성적"][f"{grade}-1기말"]
        InputGradesModal.grades3.default = last_member_data["성적"][f"{grade}-2중간"]
        InputGradesModal.grades4.default = last_member_data["성적"][f"{grade}-2기말"]
    else:
        InputGradesModal.grades1.label = f"{grade}-1중간"
        InputGradesModal.grades2.label = f"{grade}-1기말"
        InputGradesModal.grades3.label = f"{grade}-2중간"
        InputGradesModal.grades4.label = f"{grade}-2기말"
        InputGradesModal.grades1.default = None
        InputGradesModal.grades2.default = None
        InputGradesModal.grades3.default = None
        InputGradesModal.grades4.default = None
        

class Grades(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Grades Cog loaded")

    @app_commands.command(name="성적", description="성적 입력, 조회")
    async def grades(self, interaction: discord.Interaction):
        import_member_data(interaction.user.id)
        if last_member_data is not None:
            await interaction.response.send_message("원하는 활동을 선택해주세요.", view=GradesButtonView(), ephemeral=True)
        else:
            await interaction.response.send_message("정보를 먼저 등록해주세요. [/정보]", ephemeral=True)


#성적 활동 선택
class GradesButtonView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="성적 조회", style=discord.ButtonStyle.primary)
    async def read_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("성적 조회", ephemeral=True)
        self.stop()

    @discord.ui.button(label="성적 입력/수정", style=discord.ButtonStyle.primary)
    async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("성적을 입력/수정할 학년을 선택해주세요.", view=GradeButtonView(), ephemeral=True)
        self.stop()

#성적 입력 선택
class GradeButtonView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="중1 성적", style=discord.ButtonStyle.primary)
    async def select_button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        import_member_data(interaction.user.id)
        selected_grade = "중1"
        print(selected_grade)
        default_data_setting(last_member_data, selected_grade)
        await interaction.response.send_modal(InputGradesModal())
        self.stop()
    @discord.ui.button(label="중2 성적", style=discord.ButtonStyle.primary)
    async def select_button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        import_member_data(interaction.user.id)
        selected_grade = "중2"
        print(selected_grade)
        default_data_setting(last_member_data, selected_grade)
        await interaction.response.send_modal(InputGradesModal())
        self.stop()
    @discord.ui.button(label="중3 성적", style=discord.ButtonStyle.primary)
    async def select_button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        import_member_data(interaction.user.id)
        selected_grade = "중3"
        print(selected_grade)
        default_data_setting(last_member_data, selected_grade)
        await interaction.response.send_modal(InputGradesModal())
        self.stop()


#모달창에서 정보 입력
class InputGradesModal(discord.ui.Modal, title="정보 등록"):
    grade = selected_grade
    grades1 = discord.ui.TextInput(label="", placeholder="0~100 숫자만 입력 / 점수 없으면 빈칸", max_length=3, required=False)
    grades2 = discord.ui.TextInput(label="", placeholder="0~100 숫자만 입력 / 점수 없으면 빈칸", max_length=3, required=False)
    grades3 = discord.ui.TextInput(label="", placeholder="0~100 숫자만 입력 / 점수 없으면 빈칸", max_length=3, required=False)
    grades4 = discord.ui.TextInput(label="", placeholder="0~100 숫자만 입력 / 점수 없으면 빈칸", max_length=3, required=False)
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        print(interaction.data["components"][0]["components"][0]["value"])
        print(interaction.data["components"][0]["components"][0])
        print(interaction.data["components"][0]["components"])
        print(interaction.data["components"][0])
        import_member_data(interaction.user.id)
        grades_data = last_member_data["성적"]
        grades_data[f"{self.grade}-1중간"] = interaction.data["components"][0]["components"][0]["value"]
        grades_data[f"{self.grade}-1기말"] = interaction.data["components"][1]["components"][0]["value"]
        grades_data[f"{self.grade}-2중간"] = interaction.data["components"][2]["components"][0]["value"]
        grades_data[f"{self.grade}-2기말"] = interaction.data["components"][3]["components"][0]["value"]

        update_member_data(discord_id=interaction.user.id, exam_grades=grades_data)

        await interaction.response.send_message(f"{interaction.user}님의 {self.grade} 성적이 등록되었습니다.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Grades(bot), guilds=[discord.Object(id=GUILD_ID)])