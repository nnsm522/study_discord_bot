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
last_member_data = None

#DB 재호출
def call_DB():
    global db
    db = mongo_client.member

#command 호출한 사람의 데이터 불러와서 저장
def import_member_data(discord_id):
    global last_member_data
    last_member_data = db.member_data.find_one({"discord_id": discord_id})

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
    global db
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
        db.member_data.update_one(key, {"$set": data}, True)
    except Exception as e:
        print(f"error: {e}")
    else:
        call_DB()
        print("DB update Success!")

def delete_member_data(discord_id):
    try:
        db.member_data.delete_one({"discord_id": discord_id})
    except Exception as e:
        print(f"error: {e}")
    else:
        call_DB()
        print("DB delete Success!")

#정보등록,수정 시 Modal창에 기본으로 입력되어있을 값 수정
def default_data_setting(last_member_data):
    if last_member_data is not None:
        CreateStudentModal.last_member_data = last_member_data
        CreateStudentModal.name.default = last_member_data["이름"]
        CreateStudentModal.birth.default = last_member_data["생년월일"]
        CreateStudentModal.school.default = last_member_data["학교"]
        CreateStudentModal.parents_phone_number.default = last_member_data["부모님_연락처"]
        CreateStudentModal.email.default = last_member_data["이메일"]
    else:
        CreateStudentModal.last_member_data = None
        CreateStudentModal.name.default = None
        CreateStudentModal.birth.default = None
        CreateStudentModal.school.default = None
        CreateStudentModal.parents_phone_number.default = None
        CreateStudentModal.email.default = None

#정보조회 내용
def read_data(data):
    return f"""
{data["discord_name"]} 님의 정보입니다.
이름 : {data["이름"]}
생년월일 : {data["생년월일"]}
학교 : {data["학교"]}
개인 연락처 : {data["개인_연락처"]}
부모님 연락처 : {data["부모님_연락처"]}
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
        import_member_data(interaction.user.id)
        if last_member_data is not None :
            await interaction.response.send_message("이미 등록된 ID 입니다.", ephemeral=True)
        else :
            default_data_setting(last_member_data)
            await interaction.response.send_modal(CreateStudentModal())
        self.stop()
    @discord.ui.button(label="정보 수정", style=discord.ButtonStyle.primary)
    async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        import_member_data(interaction.user.id)
        if last_member_data is not None :
            default_data_setting(last_member_data)
            await interaction.response.send_modal(CreateStudentModal())
        else :
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()
    @discord.ui.button(label="정보 조회", style=discord.ButtonStyle.primary)
    async def read_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        import_member_data(interaction.user.id)
        if last_member_data is not None :
            await interaction.response.send_message(read_data(last_member_data), ephemeral=True)
        else :
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()
    @discord.ui.button(label="정보 삭제", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        import_member_data(interaction.user.id)
        if last_member_data is not None :
            await interaction.response.send_message("정보를 삭제하시면 점수, 알코인 등의 데이터는 복구되지 않습니다.", view=DeleteButtonView(), ephemeral=True)
        else:
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()


#모달창에서 정보 입력
class CreateStudentModal(discord.ui.Modal, title="정보 등록"):
    last_member_data = last_member_data
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
        if self.last_member_data is not None:
            update_member_data(
                discord_id=discord_id,
                discord_name=discord_name,
                name=name,
                birth=birth,
                school=school,
                parents_phone_number=parents_phone_number,
                email=email,
                exam_grades=last_member_data["성적"],
                r_coin=last_member_data["r_coin"]
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