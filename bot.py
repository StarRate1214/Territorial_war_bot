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
worksheet_manage = doc.worksheet('영토전-관리용')
worksheet_army = doc.worksheet('영토전-병종')

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


ok_hour = [4, 6, 8, 10, 12, 14]  # GMT 기준으로 측정되나봄 +9시간
channel = 807086592266338305
msg = "♚영☆토☆전♚참가시$\n$전원 은화☜☜공헌도100%증정※\n♜컨커러스 블레이드♜시즌미션 무료도움￥\n특정조건 §§관녕철기병§§★칸케식★\n$$고오급 전사로 승급할 절호의 기회$$\n즉시참가 영토전-참여여부 (!영토전참가)"

loop = asyncio.get_event_loop


async def looping(ctx):
    now = datetime.datetime.now()
    old_hour = now.hour
    await client.get_channel(channel).send(msg)
    while True:
        if (old_hour != now.hour) & (now.hour in ok_hour):
            old_hour = now.hour
            now = datetime.datetime.now()
            await client.get_channel(channel).send(msg)
        await asyncio.sleep(60)
        now = datetime.datetime.now()


@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return

    if ctx.content.startswith("!병종입력"):
        try:
            user = ctx.author  # 디코이름 가져오기
            Guild_member = worksheet_army.find(user.display_name)  # 이름 찾기
            pic = ctx.content[6:]
            arr = pic.split("/")
            col_num = 3
            for i in arr:
                worksheet_army.update_cell(Guild_member.row, col_num, i)
                col_num = col_num + 1
            await ctx.channel.send(f'"{user.display_name}" 병종입력 성공')
        except:
            await ctx.channel.send(f'병종입력 실패')

    if ctx.content.startswith("!흥보시작"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                await ctx.channel.send(f'지금부터 영토전 흥보를 시작함 13시-23시 2시간간격')
                client.loop.create_task(looping(ctx))

    if ctx.content.startswith("!흥보종료"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                await ctx.channel.send(f'흥보종료 성공')
                client.loop.stop

    if ctx.content.startswith("!흥보메시지"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                pic = ctx.content[7:]
                global msg
                msg = pic
                await ctx.channel.send(f'msg확인 "'+msg+'"')

    if ctx.content.startswith("!도움"):
        await ctx.channel.send('!영토전참가 or !영토전참가 [이름] |영토전 참가하기 둘 중 아무거나 사용가능\n!영토전불참 or !영토전불참 [이름] | 영토전 불참하기 둘 중 아무거나 사용가능\n !병종입력 [병종1]/[병종2]/[병종3] | 영토전에 가져오는 병종입력 최대 5')

    if ctx.content.startswith("!서버도움"):
        await ctx.channel.send('!흥보시작 | 13시-23시 2시간간격 메시지 보냄\n!흥보메시지 [메시지] | 흥보문구 변경\n!흥보종료 | 채널에 메시지보내기를 종료함')

    #print ('msg:'+message.content)
    if ctx.content.startswith("!영토전참가"):
        pic = ctx.content[7:]
        #print('pic"'+pic+'"')
        if pic != '':
            try:
                Guild_member = worksheet.find(pic)
                worksheet.update_cell(Guild_member.row, 7, "O")
                Now_member = worksheet.acell('G15').value
                await ctx.channel.send(f'"{pic}" 영토전참가 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{pic}" 이름이 없거나 틀림')
        else:
            try:
                user = ctx.author
                Guild_member = worksheet.find(user.display_name)
                worksheet.update_cell(Guild_member.row, 7, "O")
                Now_member = worksheet.acell('G15').value
                await ctx.channel.send(f'"{user.display_name}" 영토전참가 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'이름이 없거나 틀림')

    #print ('msg:'+message.content)
    if ctx.content.startswith("!영토전불참"):
        pic = ctx.content[7:]
        #print('pic"'+pic+'"')
        if pic != '':
            try:
                Guild_member = worksheet.find(pic)
                worksheet.update_cell(Guild_member.row, 7, "X")
                Now_member = worksheet.acell('G15').value
                await ctx.channel.send(f'"{pic}" 영토전불참 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{pic}" 이름이 없거나 틀림')
        else:
            try:
                user = ctx.author
                Guild_member = worksheet.find(user.display_name)
                worksheet.update_cell(Guild_member.row, 7, "X")
                Now_member = worksheet.acell('G15').value
                await ctx.channel.send(f'"{user.display_name}" 영토전불참 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'이름이 없거나 틀림')


# @client.command(name='영토전참가')
# async def roll(ctx,Inputname):#닉네임 지정해서 쓸때
#     try:
#         Guild_member = worksheet.find(Inputname)
#         worksheet.update_cell(Guild_member.row, 7, "O")
#         Now_member = worksheet.acell('G15').value
#         await ctx.send(f'"{Inputname}" 영토전참가 확인됨 [참가인원] {Now_member}명')
#     except:
#         await ctx.send(f'"{Inputname}" 이름이 없거나 틀림')


client.run(TOKEN)
