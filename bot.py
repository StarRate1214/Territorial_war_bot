# -*- coding: utf-8 -*-

##################################### 서버용 ############################################
#########################################################################################
#########################################################################################
#########################################################################################
###### 개발환경 : python 3.8.5                                                      ######
######          discord                1.0.1                                       ######
######          discord.py             1.6.0                                       ######
######          apt-get install python3-pip                                        ######
###### 모듈설치 : pip3 install setuptools --upgrade                                 ######
######          pip3 install discord                                               ######
######          pip3 install asyncio                                               ######
######          pip3 install gspread                                               ######
######          pip3 install --upgrade oauth2client                                ######
#########################################################################################
#########################################################################################
#########################################################################################

import asyncio
import discord
import os
from discord import message
from discord import channel
from discord.utils import get
import gspread
import datetime
import configparser
import json
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

global ad_task
global msg
global terrirorial_members
global teCheck

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
END_FILE = BASE_DIR+'\\..\\config.ini'
print(END_FILE)
config = configparser.ConfigParser()
config.read(END_FILE, encoding="utf8")
print(config.sections())
free_channel = int(config['settings']['I_free_channel'])#자유채팅방
manage_bot_channel = int(config['settings']['I_manage_bot_channel'])#봇관리용
terrirorial_1_channel = int(config['settings']['I_terrirorial_1_channel'])#영토전 채널 1
terrirorial_2_channel = int(config['settings']['I_terrirorial_2_channel'])#영토전 채널 2
TOKEN = config['settings']['I_TOKEN']
json_file_name = config['settings']['I_json_file_name']
spreadsheet_url = config['settings']['I_spreadsheet_url']
spreadsheet_url2 = config['settings']['I_spreadsheet_url2']
msg = config['settings']['I_msg']
ok_hour = config['settings']['I_ok_hour']
ok_hour = json.loads(ok_hour)
teCheck = '종료'
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    BASE_DIR+json_file_name, scope)
gc = gspread.authorize(credentials)

# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)
doc2 = gc.open_by_url(spreadsheet_url2)

# 시트 선택하기
worksheet = doc.worksheet('병종 시트')
worksheet_manage = doc.worksheet('영토전-관리용')
worksheet_army = doc.worksheet('영토전-병종')
worksheet_attendance = doc2.worksheet('출석부')


intents = discord.Intents.default() 
intents.members = True #sets `intents.members`
bot = commands.Bot(
    command_prefix="!", 
    intents=intents, # load the intents into commands.Bot
    help_command=None
)

@bot.event
async def on_ready():  # 봇이 실행 준비가 되었을 때 행동할 것
    print('Logged in as')
    print(bot.user.name)  # 클라이언트의 유저 이름을 출력합니다.
    print(bot.user.id)  # 클라이언트의 유저 고유 ID를 출력합니다.
    # 고유 ID는 모든 유저 및 봇이 가지고있는 숫자만으로 이루어진 ID입니다.
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('"!도움" 도움말을 볼 수 있습니다. '))

  # GMT 기준으로 측정되나봄 +9시간
loop = asyncio.get_event_loop

async def ad_looping():
    now = datetime.datetime.now()
    old_hour = now.hour
    await bot.get_channel(free_channel).send(msg)
    while True:
        if (old_hour != now.hour) & (now.hour in ok_hour):
            old_hour = now.hour
            now = datetime.datetime.now()
            await bot.get_channel(free_channel).send(msg)
        await asyncio.sleep(60)
        now = datetime.datetime.now()

# 에러 처리
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

# !도움
@bot.command(name="도움", pass_context=True)
async def _help(ctx):
    await ctx.channel.send('!가입 이름 가문명(검산,검해,검천,검훈) 레벨\n!영토전 (참가,늦참,불참) (@이름)\n!출첵 (@이름)')
    return

# !서버도움
@bot.command(name="서버도움", pass_context=True)
async def _severHelp(ctx):
    if ctx.guild:
        if ctx.author.guild_permissions.manage_messages:
            await ctx.channel.send('!흥보 (시작,종료) | 13시-23시 1시간 간격으로 메시지 보냄\n!흥보 문구 [메시지] | 흥보문구 변경\n!공지 (#채널명) [메시지] | 채팅방에 봇이 메시지를 말함\n!영토전 (종료,출석)')
    return

# !공지 #채널명 메시지
@bot.command(name="공지", pass_context=True)
@commands.has_permissions(manage_messages=True)
async def _notion(ctx, channal, *, args):
    channal = int(channal[2:-1])
    await bot.get_channel(channal).send(args)
    return

# !가입 이름 가문명 레벨 무기 가입상태
@bot.command(name="가입", pass_context=True)
async def _join(ctx, name, guild, level):
    if ctx.guild:
        if ctx.author.guild_permissions.manage_messages:
            return

    member = ctx.message.author
    rankValue = "빈 셀"
    voidColumn = 3 #직위 위치
    if guild == "검산" or guild == "검해" or guild == "검천" or guild == "검훈":
        full_name = guild + " " + name + " " + level
        try:
            await member.edit(nick=full_name)
            await member.add_roles(get(ctx.guild.roles, name='가문원['+ guild +']'))
            try:
                Guild_member = worksheet.find(name) #이름 찾기
                worksheet.update_cell(col=voidColumn,row=Guild_member.row,value='가문원['+ guild +']')
            except:
                voidValue = worksheet.find(rankValue,in_column=voidColumn)
                worksheet.update_cell(col=voidColumn,row=voidValue.row,value='가문원['+ guild +']') #직위 추가
                worksheet.update_cell(col=voidColumn+1,row=voidValue.row,value=name) #이름 추가
            
            await ctx.channel.send(f'환영합니다. <@{member.id}>님 <#812693168981540864> 읽어주시고 아래 엄지척:thumbsup: 이모지 반응 눌러주세요!\n처음이시면 <#873457208174719026> 꼭! 읽어주시기 바랍니다')
            await bot.get_channel(manage_bot_channel).send(f'새로운 가문원 등장! <@{member.id}> = \"{name}\"')    
        except Exception as err:
            await bot.get_channel(manage_bot_channel).send(err)
    else:
        await ctx.channel.send(f'<@{member.id}>님 가입 양식에 맞춰서 다시 작성 부탁드립니다. \n!가입 이름 가문명(검산,검해,검천,검훈) 레벨 주무기 가입여부(O,X) ```!가입 흰검 검해 100 창 O```')
    return

# !영토전 (참가,늦참,불참) (@이름)
@bot.command(name="영토전", pass_context=True)
async def _terrirorial(ctx, status, member: discord.Member=None):
    global teCheck
    member = member or ctx.message.author
    guild = ctx.guild
    terriCol = 10 #영토전 참가여부 위치
    if status == "참가":
        yesno = "O"
    elif status == "늦참":
        yesno = "△"
    elif status == "불참":  
        yesno = "X"
    elif status == "종료":
        if guild:
            if ctx.author.guild_permissions.manage_roles:
                teCheck = status
                role = get(guild.roles, name="영토전참가자")
                await ctx.channel.send(f'```----------- 영토전이 종료되었습니다. -----------```')
                await bot.get_channel(free_channel).send(f'```----------- 영토전이 종료되었습니다. -----------```')
                for member in guild.members:
                    if role in member.roles:
                        await member.remove_roles(role)                
                await ctx.channel.send(f'역할 제거가 완료 되었습니다.')
                await bot.get_channel(free_channel).send(f'<@&876493974133690418><@&876493974133690418><@&876493974133690418><@&876493974133690418> 영토전 참가신청 부탁드립니다.')
            else:
                await ctx.channel.send(f'<@{member.id}> 영토전을 종료할 권한이 없습니다.')
                return
    elif status == "출석" or "시작":
        if guild:
            if ctx.author.guild_permissions.manage_roles:
                teCheck = status
                print(teCheck)
                await ctx.channel.send('```----------- 금일 영토전 출석 시작 -----------```<#876548929968275486>에서 !출첵 (@이름)')
                await bot.get_channel(free_channel).send('```----------- 금일 영토전 출석 시작 -----------```<#876548929968275486>에서 !출첵 (@이름)')                
                return

    try:
        dis_name = member.display_name.split(" ")
        Guild_member = worksheet.find(dis_name[1])
        worksheet.update_cell(Guild_member.row, terriCol, yesno)
        Now_member = worksheet.acell('J4').value
        await ctx.channel.send(f'<@{member.id}> "{dis_name[1]}" 영토전 {status} 확인됨 [참가인원] {Now_member}명')
    except:
        await ctx.channel.send(f'<@{member.id}> "{dis_name[1]}" 이름이 없거나 틀림 신규 가문원이라면 <#840536404945010688>에서 확인 후 진행')

    if status == "참가":
        await member.add_roles(get(guild.roles, name="영토전참가자")) #역할 부여
    elif status == "늦참":
        await member.add_roles(get(guild.roles, name="영토전참가자"))
    elif status == "불참":
        await member.remove_roles(get(guild.roles, name="영토전참가자"))
    else:
        return

# !출첵 (@이름)
@bot.command(name="출첵", pass_context=True)
async def _attendance(ctx, member: discord.Member=None):
    if ctx.channel == 876548929968275486:
        member = member or ctx.message.author
        now = datetime.datetime.now()
        week = now.isoweekday()
        hour = now.hour
        if teCheck == "출석" or "시작" or ((week == 1 or week == 6) and (hour >= 20 and hour <= 23)):
            try:
                time = str(now)
                dis_name = member.display_name.split(" ")
                Guild_member = worksheet.find(dis_name[1])#이름 찾기
                worksheet.update_cell(col=79, row=Guild_member.row, value='TRUE')
                worksheet.update_cell(col=80, row=Guild_member.row, value=time)
                await ctx.channel.send(f'<@{member.id}>님의 출석 확인')
            except:
                await ctx.channel.send(f'<@{member.id}>님은 영토전 참가자가 아닙니다.')
        else:
            await ctx.channel.send(f'<@{member.id}>님 지금은 출석시간 아닙니다.')
    return

# !흥보 (시작,종료) | 13시-23시 2시간간격 메시지 보냄\n!흥보 문구 [메시지]
@bot.command(name="홍보", pass_context=True)
async def _promotion(ctx, status, *, adcontent):
    if ctx.guild:
        if ctx.author.guild_permissions.manage_messages:
            if status == "시작":
                ad_task = bot.loop.create_task(ad_looping())                    
                await ctx.channel.send(f'지금부터 영토전 홍보를 시작함 13시-23시 2시간간격')
                print("홍보 시작")
            elif status == "종료":
                ad_task.cancel()
                await ctx.channel.send(f'홍보종료 성공')
                print("홍보 종료")
            elif status == "문구":
                pic = adcontent
                msg = str(pic)
                config.set('settings', 'I_msg', msg)
                with open(END_FILE, 'w', encoding="utf8") as configfile:
                    config.write(configfile)
                await ctx.channel.send(f'문구 확인\n'+msg+'')
                print("홍보 문구")
            else:
                return

# 과거 command 이용없이 하드코딩한거
@bot.event 
async def on_message(ctx):
    await bot.process_commands(ctx)
    if ctx.author.bot:
        return None
    if ctx.author == bot.user:
        return

bot.run(TOKEN)
