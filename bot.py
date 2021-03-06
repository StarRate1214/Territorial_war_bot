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
import gspread
import datetime
import configparser
import json
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
END_FILE = BASE_DIR+'\\..\\config.ini'
print(END_FILE)
config = configparser.ConfigParser()
config.read(END_FILE, encoding="utf8")
print(config.sections())
free_channel = int(config['settings']['I_free_channel'])
manage_bot_channel = int(config['settings']['I_manage_bot_channel'])
terrirorial_1_channel = int(config['settings']['I_terrirorial_1_channel'])
terrirorial_2_channel = int(config['settings']['I_terrirorial_2_channel'])
rjsdml_channel = int(config['settings']['I_rjsdml_channel'])
manage_rjsdml_channel = int(config['settings']['I_manage_rjsdml_channel'])
TOKEN = config['settings']['I_TOKEN']
json_file_name = config['settings']['I_json_file_name']
spreadsheet_url = config['settings']['I_spreadsheet_url']
msg = config['settings']['I_msg']
ok_hour = config['settings']['I_ok_hour']
ok_hour = json.loads(ok_hour)

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
worksheet_event = doc.worksheet('이벤트')

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

@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return

    if ctx.content.startswith("!청소"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                number = int(ctx.content.split(" ")[1])
                await ctx.delete()
                await ctx.channel.purge(limit=number)
                await ctx.channel.send(f"{number}개의 메시지 삭제")
                
    if ctx.channel.id == rjsdml_channel:
        pic = ctx.content
        user = ctx.author
        await ctx.delete()
        await client.get_channel(rjsdml_channel).send(f"익명 : {pic}")
        await client.get_channel(manage_rjsdml_channel).send(f"건의자 : {user.display_name}```{pic}```")
        
    if ctx.content.startswith("!자유말하기"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                pic = ctx.content[7:]
                await client.get_channel(free_channel).send(pic)

    # if ctx.content.startswith("!뮤트"):
    #     if ctx.guild:
    #         if ctx.author.guild_permissions.manage_messages:
    #             role = ""
    #             for i in ctx.guild.roles:
    #                 if i.name == "뮤트":
    #                     role = i
    #                     break
    #             channel = ctx.guild.get_channel(terrirorial_1_channel)
    #             await channel.set_permissions(role, speak=False)

    if ctx.content.startswith("닉네임: "):
        pic = ctx.content[5:]
        args = pic.split('\n')
        author = ctx.author
        name = args[0]
        guild = args[1][4:]
        level = args[2][4:]
        full_name = guild + " " + name + " " + level
        try:
            await author.edit(nick=full_name)
            if name:
                await client.get_channel(manage_bot_channel).send(f"새로운 가문원 등장! \"{name}\"")
        except Exception as err:
            await client.get_channel(manage_bot_channel).send(err)

    elif ctx.content.startswith("닉네임:"):
        pic = ctx.content[4:]
        args = pic.split('\n')
        author = ctx.author
        name = args[0]
        guild = args[1][3:]
        level = args[2][3:]
        full_name = guild + " " + name + " " + level
        try:
            await author.edit(nick=full_name)
            if name:
                await client.get_channel(manage_bot_channel).send(f"새로운 가문원 등장! \"{name}\"")
        except Exception as err:
            await client.get_channel(manage_bot_channel).send(err)

    if ctx.content.startswith("닉네임 : "):
        pic = ctx.content[6:]
        args = pic.split('\n')
        author = ctx.author
        name = args[0]
        guild = args[1][5:]
        level = args[2][5:]
        full_name = guild + " " + name + " " + level
        try:
            await author.edit(nick=full_name)
            if name:
                await client.get_channel(manage_bot_channel).send(f"새로운 가문원 등장! \"{name}\"")
        except Exception as err:
            await client.get_channel(manage_bot_channel).send(err)
    
    elif ctx.content.startswith("닉네임 :"):
        pic = ctx.content[5:]
        args = pic.split('\n')
        author = ctx.author
        guild = args[1][4:]
        level = args[2][4:]
        full_name = guild + " " + name + " " + level
        try:
            await author.edit(nick=full_name)
            if name:
                await client.get_channel(manage_bot_channel).send(f"새로운 가문원 등장! \"{name}\"")
        except Exception as err:
            await client.get_channel(manage_bot_channel).send(err)

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

    if ctx.content.startswith("!홍보시작"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                await ctx.channel.send(f'지금부터 영토전 홍보를 시작함 13시-23시 2시간간격')
                global ad_task
                ad_task = client.loop.create_task(ad_looping())

    if ctx.content.startswith("!홍보종료"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                await ctx.channel.send(f'홍보종료 성공')
                ad_task.cancel()

    if ctx.content.startswith("!홍보메시지"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                pic = ctx.content[7:]
                global msg
                msg = str(pic)
                config.set('settings', 'I_msg', msg)
                print(config.get("settings", "I_msg"))
                #config['settings']['I_msg'] = msg
                with open(END_FILE, 'w', encoding="utf8") as configfile:
                    config.write(configfile)
                await ctx.channel.send(f'msg확인 "'+msg+'"')

    if ctx.content.startswith("!이벤트도움"):
        await ctx.channel.send('!이벤트필드 or !이벤트필드 [닉네임]\n!이벤트장수 or !이벤트장수 [닉네임]\n!필드이벤트취소 or !필드이벤트취소 [닉네임]\n!장수이벤트취소 or !장수이벤트취소 [닉네임]\n!이벤트취소 or !이벤트취소 [닉네임]')

    if ctx.content.startswith("!도움"):
        await ctx.channel.send('!영토전참가 or !영토전참가 [닉네임] |영토전 참가하기 둘 중 아무거나 사용가능\n!영토전불참 or !영토전불참 [닉네임] | 영토전 불참하기 둘 중 아무거나 사용가능\n !병종입력 진충/팔레르모/양양 투창 사사/... | 영토전에 가져오는 병종입력 최대 5')

    if ctx.content.startswith("!서버도움"):
        if ctx.guild:
            if ctx.author.guild_permissions.manage_messages:
                await ctx.channel.send('!흥보시작 | 13시-23시 2시간간격 메시지 보냄\n!흥보메시지 [메시지] | 흥보문구 변경\n!흥보종료 | 채널에 메시지보내기를 종료함\n!청소 [숫자] | 청소가 필요한 채널에서 입력시 해당 숫자만큼 메시지 삭제\n!자유말하기 [메시지] | 자유-채팅방에 봇이 메시지를 말함')
    
    if ctx.content.startswith("!필드이벤트취소"):
        pic = ctx.content[9:]
        if pic != '':
            try:
                Guild_member = worksheet_event.find(pic)
                worksheet_event.update_cell(Guild_member.row, 2, "")
                await ctx.channel.send(f'"{pic}" 필드 이벤트취소 확인됨')
            except:
                await ctx.channel.send(f'"{pic}" 이름없음')
        else:
            try:
                user = ctx.author
                dis_name = user.display_name.split(" ")
                Guild_member = worksheet_event.find(dis_name[1])
                worksheet_event.update_cell(Guild_member.row, 2, "")
                await ctx.channel.send(f'"{dis_name[1]}" 필드 이벤트취소 확인됨')
            except:
                await ctx.channel.send(f'"{dis_name[1]}" 이름없음')

    if ctx.content.startswith("!장수이벤트취소"):
        pic = ctx.content[9:]
        if pic != '':
            try:
                Guild_member = worksheet_event.find(pic)
                worksheet_event.update_cell(Guild_member.row, 3, "")
                await ctx.channel.send(f'"{pic}" 장수 이벤트취소 확인됨')
            except:
                await ctx.channel.send(f'"{pic}" 이름없음')
        else:
            try:
                user = ctx.author
                dis_name = user.display_name.split(" ")
                Guild_member = worksheet_event.find(dis_name[1])
                worksheet_event.update_cell(Guild_member.row, 3, "")
                await ctx.channel.send(f'"{dis_name[1]}" 장수 이벤트취소 확인됨')
            except:
                await ctx.channel.send(f'"{dis_name[1]}" 이름없음')
    
    if ctx.content.startswith("!이벤트취소"):
        pic = ctx.content[7:]
        if pic != '':
            try:
                Guild_member = worksheet_event.find(pic)
                worksheet_event.update_cell(Guild_member.row, 2, "")
                worksheet_event.update_cell(Guild_member.row, 3, "")
                await ctx.channel.send(f'"{pic}" 필드 및 장수 이벤트취소 확인됨')
            except:
                await ctx.channel.send(f'"{pic}" 이름없음')
        else:
            try:
                user = ctx.author
                dis_name = user.display_name.split(" ")
                Guild_member = worksheet_event.find(dis_name[1])
                worksheet_event.update_cell(Guild_member.row, 2, "")
                worksheet_event.update_cell(Guild_member.row, 3, "")
                await ctx.channel.send(f'"{dis_name[1]}" 이벤트취소 확인됨')
            except:
                await ctx.channel.send(f'"{dis_name[1]}" 이름없음')

    if ctx.content.startswith("!이벤트필드"):
        pic = ctx.content[7:]
        if pic != '':
            try:
                Guild_member = worksheet_event.find(pic)
                worksheet_event.update_cell(Guild_member.row, 2, "필드")
                Now_member = worksheet_event.acell('b1').value
                await ctx.channel.send(f'"{pic}" 필드 이벤트참가 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{pic}" 이름없음')
        else:
            try:
                user = ctx.author
                dis_name = user.display_name.split(" ")
                Guild_member = worksheet_event.find(dis_name[1])
                worksheet_event.update_cell(Guild_member.row, 2, "필드")
                Now_member = worksheet_event.acell('b1').value
                await ctx.channel.send(f'"{dis_name[1]}" 필드 이벤트참가 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{dis_name[1]}" 이름없음')

    if ctx.content.startswith("!이벤트장수"):
        pic = ctx.content[7:]
        if pic != '':
            try:
                Guild_member = worksheet_event.find(pic)
                worksheet_event.update_cell(Guild_member.row, 3, "장수")
                Now_member = worksheet_event.acell('c1').value
                await ctx.channel.send(f'"{pic}" 장수 이벤트참가 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{pic}" 이름없음')
        else:
            try:
                user = ctx.author
                dis_name = user.display_name.split(" ")
                Guild_member = worksheet_event.find(dis_name[1])
                worksheet_event.update_cell(Guild_member.row, 3, "장수")
                Now_member = worksheet_event.acell('c1').value
                await ctx.channel.send(f'"{dis_name[1]}" 장수 이벤트참가 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{dis_name[1]}" 이름없음')

    if ctx.content.startswith("!영토전늦참"):
        pic = ctx.content[7:]
        if pic != '':
            try:
                Guild_member = worksheet.find(pic)
                worksheet.update_cell(Guild_member.row, 10, "△")
                Now_member = worksheet.acell('J4').value
                await ctx.channel.send(f'"{pic}" 영토전늦참 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{pic}" 이름이 없거나 틀림 신규 가문원이라면 <#798112697497157632>에서 확인 후 진행')
        else:
            try:
                user = ctx.author
                dis_name = user.display_name.split(" ")
                Guild_member = worksheet.find(dis_name[1])
                worksheet.update_cell(Guild_member.row, 10, "△")
                Now_member = worksheet.acell('J4').value
                await ctx.channel.send(f'"{dis_name[1]}" 영토전늦참 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{dis_name[1]}" 이름이 없거나 틀림 신규 가문원이라면 <#798112697497157632>에서 확인 후 진행')

    if ctx.content.startswith("!영토전참가"):
        pic = ctx.content[7:]
        if pic != '':
            try:
                Guild_member = worksheet.find(pic)
                worksheet.update_cell(Guild_member.row, 10, "O")
                Now_member = worksheet.acell('J4').value
                await ctx.channel.send(f'"{pic}" 영토전참가 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{pic}" 이름이 없거나 틀림 신규 가문원이라면 <#798112697497157632>에서 확인 후 진행')
        else:
            try:
                user = ctx.author
                dis_name = user.display_name.split(" ")
                Guild_member = worksheet.find(dis_name[1])
                worksheet.update_cell(Guild_member.row, 10, "O")
                Now_member = worksheet.acell('J4').value
                await ctx.channel.send(f'"{dis_name[1]}" 영토전참가 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{dis_name[1]}" 이름이 없거나 틀림 신규 가문원이라면 <#798112697497157632>에서 확인 후 진행')

    if ctx.content.startswith("!영토전불참"):
        pic = ctx.content[7:]
        if pic != '':
            try:
                Guild_member = worksheet.find(pic)
                worksheet.update_cell(Guild_member.row, 10, "X")
                Now_member = worksheet.acell('J4').value
                await ctx.channel.send(f'"{pic}" 영토전불참 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{pic}" 이름이 없거나 틀림 신규 가문원이라면 <#798112697497157632>에서 확인 후 진행')
        else:
            try:
                user = ctx.author
                dis_name = user.display_name.split(" ")
                Guild_member = worksheet.find(dis_name[1])
                worksheet.update_cell(Guild_member.row, 10, "X")
                Now_member = worksheet.acell('J4').value
                await ctx.channel.send(f'"{dis_name[1]}" 영토전불참 확인됨 [참가인원] {Now_member}명')
            except:
                await ctx.channel.send(f'"{dis_name[1]}" 이름이 없거나 틀림 신규 가문원이라면 <#798112697497157632>에서 확인 후 진행')


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
