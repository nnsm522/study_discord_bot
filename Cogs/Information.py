import pandas as pd
import discord
from discord import app_commands
from discord.ext import commands


#######################################
###############함수 파트################
#######################################
# 1. 회원정보    2. 시험성적    3. 
file_names = ["member_info", "exam_grades"]

last_call_member_id = None
last_member_data = None

def import_member_data(file_name, id):
    global last_member_data
    if check_id(file_name, id):
        last_member_data = load_file(file_name).loc[f"'{id}"]
    else:
        last_member_data = None

#csv파일 불러오기
def load_file(file_name):
    data = pd.read_csv(f"data/{file_name}.csv")
    data.set_index('discord id', inplace=True)
    return data

#csv 파일에 등록된 id인지 확인
def check_id(file_name, id):
    data = load_file(file_name)
    if(f"'{id}" in data.index.tolist()):
        return True
    else :
        return False

#등록
def register(file_name, id, data:list):
    dataframe = load_file(file_name)
    dataframe.loc[f"'{id}"] = data
    dataframe.to_csv(f"data/{file_name}.csv", encoding='utf-8-sig')

#정보 수정
def default_CreateStudentModal(bool):
    global last_member_data
    if bool:
        CreateStudentModal.name.default = str(last_member_data["이름"])
        CreateStudentModal.birth_date.default = str(last_member_data["생년월일"])
        CreateStudentModal.school.default = str(last_member_data["학교"])
        CreateStudentModal.phone_number1.default = str(last_member_data["개인 연락처"])
        CreateStudentModal.phone_number2.default = str(last_member_data["부모님 연락처"])
    else :
        CreateStudentModal.name.default = None
        CreateStudentModal.birth_date.default = None
        CreateStudentModal.school.default = None
        CreateStudentModal.phone_number1.default = None
        CreateStudentModal.phone_number2.default = None
def default_CreatePeopleModal(bool):
    global last_member_data
    if bool:
        CreatePeopleModal.name.default = str(last_member_data["이름"])
        CreatePeopleModal.phone_number1.default = str(last_member_data["개인 연락처"])
    else :
        CreatePeopleModal.name.default = None
        CreatePeopleModal.phone_number1.default = None


#######################################
#############클래스 파트################
#######################################
class Information(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Info Cog loaded")

    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(fmt)} commands")

    @app_commands.command(name="정보", description="정보 등록, 수정, 조회, 삭제 기능")
    async def information(self, interaction: discord.Interaction):
        await interaction.response.send_message("원하는 활동을 선택해주세요.(10초)", view=InfoButtonView(), ephemeral=True)

#정보 활동 선택
class InfoButtonView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="정보 등록", style=discord.ButtonStyle.primary)
    async def create_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        import_member_data(file_names[0], interaction.user.id)
        if last_member_data is not None :
            await interaction.response.send_message("이미 등록된 ID 입니다.", ephemeral=True)
        else :
            default_CreateStudentModal(False)
            await interaction.response.send_message("역할을 선택하세요.(10초)", view=CreateButtonView(), ephemeral=True)
        self.stop()
    @discord.ui.button(label="정보 수정", style=discord.ButtonStyle.primary)
    async def update_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        import_member_data(file_names[0], interaction.user.id)
        if last_member_data is not None :
            default_CreateStudentModal(True)
            await interaction.response.send_modal(CreateStudentModal())
        else :
            default_CreateStudentModal(False)
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()
    @discord.ui.button(label="정보 조회", style=discord.ButtonStyle.primary)
    async def read_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        import_member_data(file_names[0], interaction.user.id)
        if last_member_data is not None :
            await interaction.response.send_message(last_member_data, ephemeral=True)
        else :
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()
    @discord.ui.button(label="정보 삭제", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        import_member_data(file_names[0], interaction.user.id)
        if last_member_data is not None :
            await interaction.response.send_message("정보를 삭제하시면 점수, 코인 등의 데이터는 복구되지 않습니다.", ephemeral=True)
        else:
            await interaction.response.send_message("등록되지 않은 ID 입니다. 정보를 먼저 등록해주세요.", ephemeral=True)
        self.stop()

#정보등록
#학생/일반 선택
class CreateButtonView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="학생", style=discord.ButtonStyle.green)
    async def student_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CreateStudentModal())
    @discord.ui.button(label="일반", style=discord.ButtonStyle.blurple)
    async def people_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CreatePeopleModal())

#학생 모달창에서 정보 입력
class CreateStudentModal(discord.ui.Modal, title="정보 등록(학생)"):
    name = discord.ui.TextInput(label="이름", placeholder="장수학", default="None")
    birth_date = discord.ui.TextInput(label="생년월일(주민등록번호 앞자리)", min_length=6, max_length=6, placeholder="120522", default="123456")
    school = discord.ui.TextInput(label="학교", placeholder="한국중학교", default="None")
    phone_number1 = discord.ui.TextInput(label="개인 연락처", placeholder="010-1234-5678", default="None")
    phone_number2 = discord.ui.TextInput(label="부모님 연락처", placeholder="010-1234-5678", default="None")
    async def on_submit(self, interaction: discord.Interaction) -> None:
        discord_id = str(interaction.user.id)
        discord_name = str(interaction.user)
        role = "학생"
        name = interaction.data["components"][0]["components"][0]["value"]
        birth = interaction.data["components"][1]["components"][0]["value"]
        school = interaction.data["components"][2]["components"][0]["value"]
        personal_phone_number = interaction.data["components"][3]["components"][0]["value"]
        parents_phone_number = interaction.data["components"][4]["components"][0]["value"]
        register(file_names[0], discord_id, [discord_name, role, name, birth, school, personal_phone_number, parents_phone_number])
        register(file_names[1], discord_id, [None, None, None, None, None, None, None, None, None, None, None, None])
        await interaction.response.send_message(f"{interaction.user}님의 정보가 등록되었습니다.", ephemeral=True)
#일반 모달창에서 정보입력
class CreatePeopleModal(discord.ui.Modal, title="정보 등록(일반)"):
    name = discord.ui.TextInput(label="이름", placeholder="장수학")
    phone_number1 = discord.ui.TextInput(label="연락처", placeholder="010-1234-5678")
    async def on_submit(self, interaction: discord.Interaction) -> None:
        discord_id = str(interaction.user.id)
        discord_name = str(interaction.user)
        role = "일반"
        name = interaction.data["components"][0]["components"][0]["value"]
        birth = None
        school = None
        personal_phone_number = interaction.data["components"][1]["components"][0]["value"]
        parents_phone_number = None
        register(file_names[0], discord_id, [discord_name, role, name, birth, school, personal_phone_number, parents_phone_number])
        await interaction.response.send_message(f"{interaction.user}님의 정보가 등록되었습니다.", ephemeral=True)

#삭제, 취소 버튼
class DeleteButtonView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="삭제", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        id = f"'{interaction.user.id}"
        for file_name in file_names:
            dataframe = load_file(file_name)
            dataframe.drop(id, axis=0, inplace=True)
            dataframe.to_csv(f"data/{file_name}.csv", encoding='utf-8-sig')

        await interaction.response.send_message("정보가 삭제되었습니다.")
    @discord.ui.button(label="취소", style=discord.ButtonStyle.grey)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("취소되었습니다.")

async def setup(bot):
    await bot.add_cog(Information(bot))