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
import gspread
import datetime
import time
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials


#bot token
TOKEN = ""  # 봇 토큰 값
json_file_name = '/'  # 구글에서 발급받은 키값
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

client = commands.Bot(command_prefix="", help_command=None)


@client.event
async def on_ready():  # 봇이 실행 준비가 되었을 때 행동할 것
    print('Logged in as')
    print(client.user.name)  # 클라이언트의 유저 이름을 출력합니다.
    print(client.user.id)  # 클라이언트의 유저 고유 ID를 출력합니다.
    # 고유 ID는 모든 유저 및 봇이 가지고있는 숫자만으로 이루어진 ID입니다.
    print('------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('"!도움" 도움말 호출'))


ok_hour = [4, 6, 8, 10, 12, 14]  # GMT 기준으로 측정되나봄 +9시간
channel = 810843011629842432
manage_bot_channel = 806541412505747478
msg = "21.02.20 토요일 영토전은 덕무에서 합니다. 토요일 8시 30분 \"오그리아\"에서 만나도록 합시다.\n우리 검산의 3번째 부흥을 위해 함께 힘내봅시다.  [#영토전-참여여부  !영토전참가]"

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
                global task
                task = client.loop.create_task(looping(ctx))

    if ctx.content.startswith("!흥보종료"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                await ctx.channel.send(f'흥보종료 성공')
                task.cancel()

    if ctx.content.startswith("!흥보메시지"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                pic = ctx.content[7:]
                global msg
                msg = pic
                await ctx.channel.send(f'msg확인 "'+msg+'"')

    if ctx.content.startswith("닉네임:"):
        pic = ctx.content[4:]
        args = pic.split('\n')
        author = ctx.author
        name=args[0]
        try:
            await author.edit(nick=name)
            if name:
                await client.get_channel(manage_bot_channel).send(f"새로운 가문원 등장! \"{name}\"")
        except Exception as err:
                await ctx.channel.send(err)

    if ctx.content.startswith("!청소"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                number= int(ctx.content.split(" ")[1])
                await ctx.delete()
                await ctx.channel.purge(limit=number)
                await ctx.channel.send(f"{number}개의 메시지 삭제")

    if ctx.content.startswith("!뮤트"):
                pic = ctx.content[4:22]
                author = ctx.guild.get_member(int(pic))  # 디코이름 가져오기
                role = discord.utils.get(message.Guild.roles, name="뮤트")
                await author.add_roles(role)
                await ctx.channel.send(f'"{author.display_name}" 뮤트 성공')

    if ctx.content.startswith("!도움"):
        await ctx.channel.send('!영토전참가 or !영토전참가 [닉네임] |영토전 참가하기 둘 중 아무거나 사용가능\n!영토전불참 or !영토전불참 [닉네임] | 영토전 불참하기 둘 중 아무거나 사용가능\n !병종입력 [병종1]/[병종2]/[병종3] | 영토전에 가져오는 병종입력 최대 5')

    if ctx.content.startswith("!서버도움"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                await ctx.channel.send('!흥보시작 | 13시-23시 2시간간격 메시지 보냄\n!흥보메시지 [메시지] | 흥보문구 변경\n!흥보종료 | 채널에 메시지보내기를 종료함\n!청소 [숫자] | 청소가 필요한 채널에서 입력시 해당 숫자만큼 메시지 삭제')

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
                await ctx.channel.send(f'"{pic}" 이름이 없거나 틀림 신규 가문원이라면 #병종-시트에서 확인 후 진행')
        else:
            try:
                user = ctx.author
                Guild_member = worksheet.find(user.display_name)
                worksheet.update_cell(Guild_member.row, 7, "O")
                Now_member = worksheet.acell('G15').value
                await ctx.channel.send(f'"{user.display_name}" 영토전참가 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'이름이 없거나 틀림 신규 가문원이라면 #병종-시트에서 확인 후 진행')

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
