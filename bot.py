# -*- coding: utf-8 -*- 

##################################### 서버용 V12  #########################################
#########################################################################################
#########################################################################################
#########################################################################################
###### 개발환경 : python 3.8.5											    		 ######
######			discord                1.0.1                                       ######
######			discord.py             1.6.0 						     		   ######
######          apt-get install python3-pip                                        ######
###### 모듈설치 : pip3 install setuptools --upgrade									 ######
######			pip3 install discord											   ######
######			pip3 install asyncio           									   ######
######			pip3 install gspread											   ######
######			pip3 install --upgrade oauth2client								   ######
#########################################################################################
#########################################################################################
#########################################################################################

import discord
import os
import gspread
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials


#bot token
TOKEN = "" #봇 토큰 값
json_file_name = '/'#구글에서 발급받은 키값
spreadsheet_url = ''#시트의 주소


scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


credentials = ServiceAccountCredentials.from_json_keyfile_name(BASE_DIR+json_file_name, scope)
gc = gspread.authorize(credentials)



# 스프레스시트 문서 가져오기 
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet = doc.worksheet('병종 시트')

#Guild_member = worksheet.range('D15:D114')
#print(Guild_member)

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready(): # 봇이 실행 준비가 되었을 때 행동할 것
    print('Logged in as')
    print(client.user.name) # 클라이언트의 유저 이름을 출력합니다.
    print(client.user.id) # 클라이언트의 유저 고유 ID를 출력합니다.
    # 고유 ID는 모든 유저 및 봇이 가지고있는 숫자만으로 이루어진 ID입니다.
    print('------')
    await client.change_presence(status = discord.Status.online, activity = discord.Game('"!도움" 도움말 호출'))

@client.command(name='도움')
async def roll(ctx):
    await ctx.send('!영토전참가 [이름]\n!영토전불참 [이름]\n명령어는붙이고 이름 앞은 띄어쓰기')

# @client.command(name='영토전참가')
# async def roll(ctx, Inputname):
#     Guild_member = worksheet.find(Inputname)
#     if worksheet.find(Inputname):
#         worksheet.update_cell(Guild_member.row,7,"O")
#         await ctx.send(f'"{Inputname}" 영토전참가 확인됨')#구글 시트에서 그때그때 찾아서 바꾸는걸로 
#     else:
#         await ctx.send(f'"{Inputname}" 이름이 없거나 틀림')


@client.command(name='영토전참가')
async def roll(ctx, Inputname):
    Guild_member = worksheet.find(Inputname)
    if worksheet.find(Inputname):
        worksheet.update_cell(Guild_member.row,7,"O")
        Now_member = worksheet.acell('G14').value
        await ctx.send(f'"{Inputname}" 영토전참가 확인됨 [참가인원] {Now_member}명')#구글 시트에서 그때그때 찾아서 바꾸는걸로 
    else:
        await ctx.send(f'"{Inputname}" 이름이 없거나 틀림')

@client.command(name='영토전불참')
async def roll(ctx, Inputname):
    Guild_member = worksheet.find(Inputname)
    if worksheet.find(Inputname):
        worksheet.update_cell(Guild_member.row,7,"X")
        await ctx.send(f'"{Inputname}" 영토전불참 확인됨 [참가인원] {Now_member}명')
    else: 
        await ctx.send(f'"{Inputname}" 이름이 없거나 틀림')

client.run(TOKEN)
