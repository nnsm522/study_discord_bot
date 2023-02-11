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


#command 호출한 사람의 데이터 불러와서 저장
def import_member_data(discord_id):
    try:
        mongo_client = pymongo.MongoClient(MONGO_URL)
        db = mongo_client.member
        data = db.member_data.find_one({"discord_id": discord_id})
    except Exception as e:
        print(e)
    else:
        mongo_client.close()
        return data

def update_member_data(discord_id, discord_name,
        name, birth, school, parents_phone_number, email,
        exam_grades={
            "중1-1중간": None,
            "중1-1기말": None,
            "중1-2중간": None,
            "중1-2기말": None,
            "중2-1중간": None,
            "중2-1기말": None,
            "중2-2중간": None,
            "중2-2기말": None,
            "중3-1중간": None,
            "중3-1기말": None,
            "중3-2중간": None,
            "중3-2기말": None,
        }, r_coin=0):
    key = {"discord_id": discord_id}
    data = {
        "discord_id": discord_id,
        "discord_name": discord_name,
        "이름": name,
        "생년월일": birth,
        "학교": school,
        "부모님_연락처": parents_phone_number,
        "이메일": email,
        "성적": exam_grades,
        "r_coin": r_coin
    }
    try:
        mongo_client = pymongo.MongoClient(MONGO_URL)
        db = mongo_client.member
        db.member_data.update_one(key, {"$set": data}, True)
    except Exception as e:
        print(f"error: {e}")
    else:
        mongo_client.close()
        print("DB update Success!")

def delete_member_data(discord_id):
    try:
        mongo_client = pymongo.MongoClient(MONGO_URL)
        db = mongo_client.member
        db.member_data.delete_one({"discord_id": discord_id})
    except Exception as e:
        print(f"error: {e}")
    else:
        mongo_client.close()
        print("DB delete Success!")

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
        member_data = import_member_data(interaction.user.id)
        if member_data is not None :
            await interaction.response.send_message("이미 등록된 ID 입니다.", ephemeral=True)
        else :
            modal = InputInformationModal()
            default_data_setting(modal, member_data)
            await interaction.response.send_modal(modal)
        self.stop()
    @discord.ui.button(label="정보 수정", style=discord.ButtonStyle.primary)
    async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_data = import_member_data(interaction.user.id)
        if member_data is not None :
            modal = InputInformationModal()
            default_data_setting(modal, member_data)
            await interaction.response.send_modal(modal)
        else :
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()
    @discord.ui.button(label="정보 조회", style=discord.ButtonStyle.primary)
    async def read_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_data = import_member_data(interaction.user.id)
        if member_data is not None :
            await interaction.response.send_message(read_data(member_data), ephemeral=True)
        else :
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()
    @discord.ui.button(label="정보 삭제", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member_data = import_member_data(interaction.user.id)
        if member_data is not None :
            view = DeleteButtonView()
            await interaction.response.send_message("정보를 삭제하시면 점수, 알코인 등의 데이터는 복구되지 않습니다.", view=DeleteButtonView(), ephemeral=True)
        else:
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()


#모달창에서 정보 입력
class InputInformationModal(discord.ui.Modal, title="정보 등록"):
    member_data = {
        "discord_id": None,
        "discord_name": None,
        "이름": None,
        "생년월일": None,
        "학교": None,
        "부모님_연락처": None,
        "이메일": None,
        "성적": None,
        "r_coin": None
    }
    name = discord.ui.TextInput(label="이름", placeholder="장수학", max_length=15)
    birth = discord.ui.TextInput(label="생년월일(주민등록번호 앞자리)", min_length=6, max_length=6, placeholder="120522")
    school = discord.ui.TextInput(label="학교", placeholder="한국중학교", max_length=15, required=False)
    parents_phone_number = discord.ui.TextInput(label="부모님 연락처", placeholder="010-1234-5678", min_length=10, max_length=15, required=False)
    email = discord.ui.TextInput(label="구글 클래스룸 이메일", placeholder="r_math123@gmail.com")
    async def on_submit(self, interaction: discord.Interaction) -> None:
        discord_id = interaction.user.id
        discord_name = str(interaction.user)
        name = interaction.data["components"][0]["components"][0]["value"]
        birth = interaction.data["components"][1]["components"][0]["value"]
        school = interaction.data["components"][2]["components"][0]["value"]
        parents_phone_number = interaction.data["components"][3]["components"][0]["value"]
        email = interaction.data["components"][4]["components"][0]["value"]
        if self.member_data is not None:
            update_member_data(
                discord_id=discord_id,
                discord_name=discord_name,
                name=name,
                birth=birth,
                school=school,
                parents_phone_number=parents_phone_number,
                email=email,
                exam_grades=self.member_data["성적"],
                r_coin=self.member_data["r_coin"]
            )
        else:
            update_member_data(
                discord_id=discord_id,
                discord_name=discord_name,
                name=name,
                birth=birth,
                school=school,
                parents_phone_number=parents_phone_number,
                email=email,
            )
        #학생 역할 부여
        await interaction.user.add_roles(get(interaction.guild.roles, name="학생"))
        await interaction.response.send_message(f"{interaction.user}님의 정보가 등록되었습니다.", ephemeral=True)

#삭제, 취소 버튼
class DeleteButtonView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="삭제", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        delete_member_data(interaction.user.id)
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