# -*- coding: utf-8 -*-

##################################### 서버용  #########################################
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
msg = config['settings']['I_msg']
ok_hour = config['settings']['I_ok_hour']
ok_hour = json.loads(ok_hour)
terrirorial_members = config['settings']['I_terrirorial_members']

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    BASE_DIR+json_file_name, scope)
gc = gspread.authorize(credentials)

# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet = doc.worksheet('병종 시트')
worksheet_manage = doc.worksheet('영토전-관리용')
worksheet_army = doc.worksheet('영토전-병종')
#worksheet_event = doc.worksheet('이벤트')

#Guild_member = worksheet.range('D15:D114')
#print(Guild_member)

client = commands.Bot(command_prefix="!", help_command=None)

@client.event
async def on_ready():  # 봇이 실행 준비가 되었을 때 행동할 것
    print('Logged in as')
    print(client.user.name)  # 클라이언트의 유저 이름을 출력합니다.
    print(client.user.id)  # 클라이언트의 유저 고유 ID를 출력합니다.
    # 고유 ID는 모든 유저 및 봇이 가지고있는 숫자만으로 이루어진 ID입니다.
    print('------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('"!도움" 도움말 호출'))

  # GMT 기준으로 측정되나봄 +9시간
loop = asyncio.get_event_loop

async def ad_looping():
    now = datetime.datetime.now()
    old_hour = now.hour
    await client.get_channel(free_channel).send(msg)
    while True:
        if (old_hour != now.hour) & (now.hour in ok_hour):
            old_hour = now.hour
            now = datetime.datetime.now()
            await client.get_channel(free_channel).send(msg)
        await asyncio.sleep(60)
        now = datetime.datetime.now()

#에러 처리
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

#도움
@client.command(name="도움", pass_context=True)
async def _help(ctx):
    await ctx.channel.send('!가입 이름 가문[검산|검해] 레벨 주무기 가입상태[O|X] \n!영토전 [참가|늦참|불참] (@이름)')

#서버도움
@client.command(name="서버도움", pass_context=True)
async def _severHelp(ctx):
    if ctx.guild:
        if ctx.author.guild_permissions.manage_messages:
            await ctx.channel.send('!흥보 [시작|종료] | 13시-23시 2시간간격 메시지 보냄\n!흥보 문구 (메시지) | 흥보문구 변경\n!자유말하기 [메시지] | 자유-채팅방에 봇이 메시지를 말함')

# async def _terrirorial(ctx):
#     role = ctx.guild.get_role(813827862649372673)
#     print(role)
#     print(role.members)
#     # Going through every member and pinging him
#     for member in role.members:
#         await ctx.send(member.mention)
#guild = ctx.message.guild 서버이름

@client.command(name="자유채팅", pass_context=True)
async def _freeChat(ctx, *, args):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                await client.get_channel(free_channel).send(args)

#!가입 이름 가문 레벨 무기 가입상태
#!가입 1등항해사 [검산|검해] 300 창 [O|X]
@client.command(name="가입", pass_context=True)
async def _join(ctx, name, guild, level):
    author = ctx.author
    full_name = guild + " " + name + " " + level
    try:
        await author.edit(nick=full_name)
        if name:
            await client.get_channel(manage_bot_channel).send(f"새로운 가문원 등장! \"{name}\"")
    except Exception as err:
        await client.get_channel(manage_bot_channel).send(err)

@client.command(name="영토전", pass_context=True)
async def _terrirorial(ctx, status, member: discord.Member=None):
    member = member or ctx.message.author

    if status == "참가":
        yesno = "O"
    elif status == "늦참":
        yesno = "△"
    elif status == "불참":
        yesno = "X"
    elif status == "종료":
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                print("영토전 종료")
    try:
        member = member or ctx.message.author
        dis_name = member.display_name.split(" ")
        Guild_member = worksheet.find(dis_name[1])
        worksheet.update_cell(Guild_member.row, 10, yesno)
        Now_member = worksheet.acell('J4').value
        await ctx.channel.send(f'"{dis_name[1]}" 영토전 {status} 확인됨 [참가인원] {Now_member}명')
    except:
        await ctx.channel.send(f'"{dis_name[1]}" 이름이 없거나 틀림 신규 가문원이라면 <#840536404945010688>에서 확인 후 진행')

    if status == "참가":
        await member.add_roles(get(ctx.guild.roles, name="영토전참가자")) #역할 부여
        terrirorial_members = config['settings']['I_terrirorial_members']
        terrirorial_members = terrirorial_members +', \"'+ str(member.id) +'\"'#문자열 끝에 추가
        config.set('settings', 'I_terrirorial_members', terrirorial_members)
        with open(END_FILE, 'w', encoding="utf8") as configfile: #파일 입력
            config.write(configfile)
        
    elif status == "늦참":
        await member.add_roles(get(ctx.guild.roles, name="영토전참가자"))
        terrirorial_members = config['settings']['I_terrirorial_members']
        terrirorial_members = terrirorial_members +', \"'+ str(member.id) +'\"'#문자열 끝에 추가
        config.set('settings', 'I_terrirorial_members', terrirorial_members)
        with open(END_FILE, 'w', encoding="utf8") as configfile: #파일 입력
            config.write(configfile)

    elif status == "불참":
        await member.remove_roles(get(ctx.guild.roles, name="영토전참가자"))

    else:
        return

@client.command(name="홍보", pass_context=True)
async def _promotion(ctx, status, *, adcontent):
    if ctx.guild:
        if ctx.author.guild_permissions.manage_messages:
            if status == "시작":
                ad_task = client.loop.create_task(ad_looping())                    
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

@client.event 
async def on_message(ctx):
    await client.process_commands(ctx)
    if ctx.author.bot:
        return None
    if ctx.author == client.user:
        return

client.run(TOKEN)
