import os
from dotenv import load_dotenv
import pymongo
import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import db_module

load_dotenv(".env")
MONGO_URL = os.getenv('MONGO_URL')
GUILD_ID = os.getenv('GUILD_ID')


#정보등록,수정 시 Modal창에 기본으로 입력되어있을 값 수정
def default_data_setting(modal, member_data):
    if member_data is not None:
        modal.member_data = member_data
        modal.name.default = member_data["이름"]
        modal.birth.default = member_data["생년월일"]
        modal.school.default = member_data["학교"]
        modal.parents_phone_number.default = member_data["부모님_연락처"]
        modal.email.default = member_data["이메일"]
    else:
        modal.member_data = None
        modal.name.default = None
        modal.birth.default = None
        modal.school.default = None
        modal.parents_phone_number.default = None
        modal.email.default = None

#정보조회 내용
def read_data(data):
    return f"""
{data["discord_name"]} 님의 정보입니다.
『　이　　름　』　:　【 {data["이름"]} 】
『　생년월일　』　:　【 {data["생년월일"]} 】
『　학　　교　』　:　【 {data["학교"]} 】
『부모님연락처』　:　【 {data["부모님_연락처"]} 】
『이메일　주소』　:　【 {data["이메일"]} 】
"""


class Information(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Info Cog loaded")

    @app_commands.command(name="정보", description="정보 등록, 수정, 조회, 삭제 기능")
    async def information(self, interaction: discord.Interaction):
        await interaction.response.send_message("원하는 활동을 선택해주세요.", view=InfoButtonView(), ephemeral=True)

#정보 활동 선택
class InfoButtonView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="정보 등록", style=discord.ButtonStyle.primary)
    async def create_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_data = db_module.import_member_data(interaction.user.id)
        if member_data is not None :
            await interaction.response.send_message("이미 등록된 ID 입니다.", ephemeral=True)
        else :
            modal = InputInformationModal()
            default_data_setting(modal, member_data)
            await interaction.response.send_modal(modal)
        self.stop()
    @discord.ui.button(label="정보 수정", style=discord.ButtonStyle.primary)
    async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_data = db_module.import_member_data(interaction.user.id)
        if member_data is not None :
            modal = InputInformationModal()
            default_data_setting(modal, member_data)
            await interaction.response.send_modal(modal)
        else :
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()
    @discord.ui.button(label="정보 조회", style=discord.ButtonStyle.primary)
    async def read_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_data = db_module.import_member_data(interaction.user.id)
        if member_data is not None :
            await interaction.response.send_message(read_data(member_data), ephemeral=True)
        else :
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()
    @discord.ui.button(label="정보 삭제", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_data = db_module.import_member_data(interaction.user.id)
        if member_data is not None :
            view = DeleteButtonView()
            await interaction.response.send_message("정보를 삭제하시면 점수, 알코인 등의 데이터는 복구되지 않습니다.", view=view, ephemeral=True)
        else:
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()


#모달창에서 정보 입력
class InputInformationModal(discord.ui.Modal, title="정보 등록"):
    member_data = None
    name = discord.ui.TextInput(label="이름", placeholder="장수학", max_length=15)
    birth = discord.ui.TextInput(label="생년월일(주민등록번호 앞자리)", min_length=6, max_length=6, placeholder="120522")
    school = discord.ui.TextInput(label="학교", placeholder="한국중학교", max_length=15, required=False)
    parents_phone_number = discord.ui.TextInput(label="부모님 연락처", placeholder="010-1234-5678", min_length=10, max_length=15, required=False)
    email = discord.ui.TextInput(label="구글 클래스룸 이메일", placeholder="r_math123@gmail.com")
    async def on_submit(self, interaction: discord.Interaction) -> None:
        if self.member_data is None:
            self.member_data = db_module.member_data_model()

        self.member_data["discord_id"] = interaction.user.id
        self.member_data["discord_name"] = str(interaction.user)
        self.member_data["이름"] = interaction.data["components"][0]["components"][0]["value"]
        self.member_data["생년월일"] = interaction.data["components"][1]["components"][0]["value"]
        self.member_data["학교"] = interaction.data["components"][2]["components"][0]["value"]
        self.member_data["부모님_연락처"] = interaction.data["components"][3]["components"][0]["value"]
        self.member_data["이메일"] = interaction.data["components"][4]["components"][0]["value"]
        
        db_module.update_member_data(self.member_data)

        #학생 역할 부여
        await interaction.user.add_roles(get(interaction.guild.roles, name="학생"))
        await interaction.response.send_message(f"{interaction.user}님의 정보가 등록되었습니다.", ephemeral=True)

#삭제, 취소 버튼
class DeleteButtonView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="삭제", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        db_module.delete_member_data(interaction.user.id)
        #역할 모두 삭제
        for role in interaction.user.roles:
            if(str(role) == "@everyone"):
                pass
            else:
                await interaction.user.remove_roles(get(interaction.user.roles, name=str(role)))
        await interaction.response.send_message("정보가 삭제되었습니다.", ephemeral=True)
    @discord.ui.button(label="취소", style=discord.ButtonStyle.grey)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("취소되었습니다.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Information(bot), guilds=[discord.Object(id=GUILD_ID)])