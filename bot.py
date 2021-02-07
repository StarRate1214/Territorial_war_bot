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
import gspread
import datetime
import time
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials



#bot token
TOKEN = ""  # 봇 토큰 값
json_file_name = ''  # 구글에서 발급받은 키값
spreadsheet_url = ''  # 시트의 주소


scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    BASE_DIR+json_file_name, scope)
gc = gspread.authorize(credentials)


# 스프레스시트 문서 가져오기
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet = doc.worksheet('병종 시트')

#Guild_member = worksheet.range('D15:D114')
#print(Guild_member)

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():  # 봇이 실행 준비가 되었을 때 행동할 것
    print('Logged in as')
    print(client.user.name)  # 클라이언트의 유저 이름을 출력합니다.
    print(client.user.id)  # 클라이언트의 유저 고유 ID를 출력합니다.
    # 고유 ID는 모든 유저 및 봇이 가지고있는 숫자만으로 이루어진 ID입니다.
    print('------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('"!도움" 도움말 호출'))


@client.command(name='도움')
async def roll(ctx):
    await ctx.send('!영토전참가 [이름]\n!영토전불참 [이름]')

@client.command(name='영토전참가')
async def roll(ctx,Inputname):#닉네임 지정해서 쓸때
    try:
        Guild_member = worksheet.find(Inputname)
        worksheet.update_cell(Guild_member.row, 7, "O")
        Now_member = worksheet.acell('G15').value
        await ctx.send(f'"{Inputname}" 영토전참가 확인됨 [참가인원] {Now_member}명')
    except:
        await ctx.send(f'"{Inputname}" 이름이 없거나 틀림')


# async def roll(ctx):  # 뒤에 없을때
#     try:
#         user = ctx.author
#         Guild_member = worksheet.find(user.display_name)
#         worksheet.update_cell(Guild_member.row, 7, "O")
#         Now_member = worksheet.acell('G15').value
#         await ctx.send(f'"{user.display_name}" 영토전참가 확인됨 [참가인원] {Now_member}명')
#     except:
#         await ctx.send(f'이름이 없거나 틀림')

@client.command(name='영토전불참')
async def roll(ctx,Inputname):
    try:
        Guild_member = worksheet.find(Inputname)
        worksheet.update_cell(Guild_member.row, 7, "X")
        Now_member = worksheet.acell('G15').value
        await ctx.send(f'"{Inputname}" 영토전불참 확인됨 [참가인원] {Now_member}명')
    except:
        await ctx.send(f'"{Inputname}" 이름이 없거나 틀림')


ok_hour = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]#  GMT 기준으로 측정되나봄
channel = 807086592266338305 #채널코드
msg = "♚영☆토☆전♚참가시$\n$전원 은화☜☜공헌도100%증정※\n ♜컨커러스 블레이드♜시즌미션 무료도움￥\n 특정조건 §§관녕철기병§§★칸케식★\n@@앙카디아 수복기회@@ \n$$고오급 전사로 승급할 절호의 기회$$\n즉시참가 영토전-참여여부 (!영토전참가)"
loop = asyncio.get_event_loop

async def looping(ctx):
    now = datetime.datetime.now()
    old_hour = now.hour
    while True:
        if (old_hour != now.hour) & (now.hour in ok_hour):
                    old_hour = now.hour
                    now = datetime.datetime.now()
                    await client.get_channel(channel).send(msg)
        await asyncio.sleep(60)
        now = datetime.datetime.now()

@client.command(name='흥보시작')
async def alarm(ctx):
    if ctx.guild:
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.send(f'지금부터 영토전 흥보를 시작함 13시-23시 1시간간격')
            client.loop.create_task(looping(ctx))

client.run(TOKEN)
