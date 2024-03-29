import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import db_module

load_dotenv(".env")
GUILD_ID = os.getenv('GUILD_ID')


#t성적 입력/수정 시 Modal창에 기본으로 입력되어있을 값 수정
def default_data_setting(modal: discord.ui.Modal, member_data, grade):
    if member_data is not None:
        modal.member_data = member_data
        modal.grade = grade
        modal.grades1.label = f"{grade}-1중간"
        modal.grades2.label = f"{grade}-1기말"
        modal.grades3.label = f"{grade}-2중간"
        modal.grades4.label = f"{grade}-2기말"
        modal.grades1.default = member_data["성적"][f"{grade}-1중간"]
        modal.grades2.default = member_data["성적"][f"{grade}-1기말"]
        modal.grades3.default = member_data["성적"][f"{grade}-2중간"]
        modal.grades4.default = member_data["성적"][f"{grade}-2기말"]
    else:
        modal.member_data = member_data
        modal.grade = grade
        modal.grades1.label = f"{grade}-1중간"
        modal.grades2.label = f"{grade}-1기말"
        modal.grades3.label = f"{grade}-2중간"
        modal.grades4.label = f"{grade}-2기말"
        modal.grades1.default = None
        modal.grades2.default = None
        modal.grades3.default = None
        modal.grades4.default = None
        
#정보조회 내용
def read_data(data):
    return f"""
{data["discord_name"]} 님의 성적입니다.
중1-1중간 : {"없음" if data["성적"]["중1-1중간"] is None else data["성적"]["중1-1중간"]}
중1-1기말 : {"없음" if data["성적"]["중1-1기말"] is None else data["성적"]["중1-1기말"]}
중1-2중간 : {"없음" if data["성적"]["중1-2중간"] is None else data["성적"]["중1-2중간"]}
중1-2기말 : {"없음" if data["성적"]["중1-2기말"] is None else data["성적"]["중1-2기말"]}
중2-1중간 : {"없음" if data["성적"]["중2-1중간"] is None else data["성적"]["중2-1중간"]}
중2-1기말 : {"없음" if data["성적"]["중2-1기말"] is None else data["성적"]["중2-1기말"]}
중2-2중간 : {"없음" if data["성적"]["중2-2중간"] is None else data["성적"]["중2-2중간"]}
중2-2기말 : {"없음" if data["성적"]["중2-2기말"] is None else data["성적"]["중2-2기말"]}
중3-1중간 : {"없음" if data["성적"]["중3-1중간"] is None else data["성적"]["중3-1중간"]}
중3-1기말 : {"없음" if data["성적"]["중3-1기말"] is None else data["성적"]["중3-1기말"]}
중3-2중간 : {"없음" if data["성적"]["중3-2중간"] is None else data["성적"]["중3-2중간"]}
중3-2기말 : {"없음" if data["성적"]["중3-2기말"] is None else data["성적"]["중3-2기말"]}
"""

class Grades(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Grades Cog loaded")

    @app_commands.command(name="성적", description="성적 입력, 조회")
    async def grades(self, interaction: discord.Interaction):
        member_data = db_module.import_member_data(interaction.user.id)
        if member_data is not None:
            view = GradesButtonView()
            view.member_data = member_data
            await interaction.response.send_message("원하는 활동을 선택해주세요.", view=view, ephemeral=True)
        else:
            await interaction.response.send_message("정보를 먼저 등록해주세요. [/정보]", ephemeral=True)


#성적 활동 선택
class GradesButtonView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    member_data = None
    @discord.ui.button(label="성적 조회", style=discord.ButtonStyle.primary)
    async def read_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(read_data(self.member_data), ephemeral=True)
        self.stop()

    @discord.ui.button(label="성적 입력/수정", style=discord.ButtonStyle.primary)
    async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = GradeButtonView()
        view.member_data = self.member_data
        await interaction.response.send_message("성적을 입력/수정할 학년을 선택해주세요.", view=view, ephemeral=True)
        self.stop()

#성적 입력할 학년 선택
class GradeButtonView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    member_data = None
    @discord.ui.button(label="중1 성적", style=discord.ButtonStyle.primary)
    async def select_button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = InputGradesModal()
        default_data_setting(modal, self.member_data, "중1")
        await interaction.response.send_modal(modal)
        self.stop()
    @discord.ui.button(label="중2 성적", style=discord.ButtonStyle.primary)
    async def select_button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = InputGradesModal()
        default_data_setting(modal, self.member_data, "중2")
        await interaction.response.send_modal(modal)
        self.stop()
    @discord.ui.button(label="중3 성적", style=discord.ButtonStyle.primary)
    async def select_button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = InputGradesModal()
        default_data_setting(modal, self.member_data, "중3")
        await interaction.response.send_modal(modal)
        self.stop()


#모달창에서 정보 입력
class InputGradesModal(discord.ui.Modal, title="정보 등록"):
    grade = None
    grades1 = discord.ui.TextInput(label="", placeholder="0~100 숫자만 입력 / 점수 없으면 빈칸", max_length=3, required=False)
    grades2 = discord.ui.TextInput(label="", placeholder="0~100 숫자만 입력 / 점수 없으면 빈칸", max_length=3, required=False)
    grades3 = discord.ui.TextInput(label="", placeholder="0~100 숫자만 입력 / 점수 없으면 빈칸", max_length=3, required=False)
    grades4 = discord.ui.TextInput(label="", placeholder="0~100 숫자만 입력 / 점수 없으면 빈칸", max_length=3, required=False)
    member_data = None
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.member_data["성적"][f"{self.grade}-1중간"] = interaction.data["components"][0]["components"][0]["value"]
        self.member_data["성적"][f"{self.grade}-1기말"] = interaction.data["components"][1]["components"][0]["value"]
        self.member_data["성적"][f"{self.grade}-2중간"] = interaction.data["components"][2]["components"][0]["value"]
        self.member_data["성적"][f"{self.grade}-2기말"] = interaction.data["components"][3]["components"][0]["value"]

        db_module.update_member_data(self.member_data)

        await interaction.response.send_message(f"{interaction.user}님의 {self.grade} 성적이 등록되었습니다.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Grades(bot), guilds=[discord.Object(id=GUILD_ID)])