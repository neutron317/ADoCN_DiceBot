#!/usr/bin/env python3
import random
import re
import discord
import dice
import logging
import os
import requests
import time
from dotenv import load_dotenv
from keep_alive import keep_alive

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

TOKEN = os.getenv("TOKEN")
RENDER_ID = os.getenv("RENDER_ID")
API_KEY = os.getenv("API_KEY")

client = discord.Client(intents=intents)

def suspend_render():
    if not RENDER_ID or not API_KEY:
        print("IDかキーがセットされていません。Suspendをスキップします。")
        return
    
    url = f"https://api.render.com/v1/services/{RENDER_ID}/suspend"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    print("----------RenderにSuspendのリクエストを送信----------")
    response = requests.post(url, headers = headers)

    if response.status_code == 204:
        print("Suspendに成功しました。")
    else:
        print(f"Suspendに失敗しました: ステータスコード {response.status_code}")
        print(response.text)

@client.event
async def on_ready():
    print(f'----------{client.user}のログインに成功----------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif re.match(r'^!d66', message.content): # !d66 d66を振る
        result = dice.d66()
        answer = '```d66 > {0}```'.format(result)
        await message.channel.send(answer) 

    elif re.match(r'!(\d+)d([+-]\d+)*(\s+.*)?$', message.content): # !2d+a+b+... 2d+a+bの結果を返す
        matched = re.match(r'!(\d+)d([+-]\d+)*(\s+.*)?$', message.content)
        rollnum = int(re.findall(r'\d+', message.content)[0])
        sumnums = dice.sumnumbers(matched)

        result = dice.roll(rollnum)

        rollres_txt = '['
        rollres_sum = 0

        for i in range(rollnum):
            rollres_sum += result[i]
            rollres_txt += str(result[i])
            if i < rollnum - 1:
                rollres_txt += ','
        rollres_txt += ']'

        answer = '```{0}d{1} > {2}{3}{1} > {4}'.format(rollnum, sumnums[0], rollres_sum, rollres_txt, rollres_sum + sumnums[1]) # 返答を生成

        if rollnum == 2:
            if rollres_sum == 2:
                answer += '(自動失敗:0)```'

            elif rollres_sum == 12:
                answer += '(自動成功:{0})```'.format(rollres_sum + sumnums[1] + 5)

            else:
                answer += '```'
        else:
            answer += '```'
            
        await message.channel.send(answer)
    
    elif re.match(r'^!pdori', message.content): # プレシャスデイズ出自表
        result = dice.d66table('table/PreciousDays/origin_table.csv')
        answer = '```プレシャスデイズ出自表 > {0} > {1} \r {2}```'.format(result[0], result[2], result[3]) # 返答を生成

        await message.channel.send(answer)

    elif re.match(r'^!pdsec', message.content): # プレシャスデイズ秘密表
        result = dice.d66table('table/PreciousDays/secret_table.csv')
        answer = '```プレシャスデイズ秘密表 > {0} > {1} \r {2}```'.format(result[0], result[2], result[3]) # 返答を生成

        await message.channel.send(answer)

    elif re.match(r'^!pdfut', message.content): # プレシャスデイズ未来表
        result = dice.d66table('table/PreciousDays/future_table.csv')
        answer = '```プレシャスデイズ未来表 > {0} > {1} \r {2}```'.format(result[0], result[2], result[3]) # 返答を生成

        await message.channel.send(answer)

    elif re.match(r'^!pdmal', message.content): # プレシャスデイズ男性名前表
        result = dice.d66table('table/PreciousDays/male_name_table.csv')
        answer = '```プレシャスデイズ男性名前表 > {0} > {1}```'.format(result[0], result[2]) # 返答を生成

        await message.channel.send(answer)

    elif re.match(r'^!pdfem', message.content): # プレシャスデイズ女性名前表
        result = dice.d66table('table/PreciousDays/female_name_table.csv')
        answer = '```プレシャスデイズ女性名前表 > {0} > {1}```'.format(result[0], result[2]) # 返答を生成

        await message.channel.send(answer)

    elif re.match(r'^!pdfam', message.content): # プレシャスデイズ家名名前表
        result = dice.d66table('table/PreciousDays/family_name_table.csv')
        answer = '```プレシャスデイズ家名名前表 > {0} > {1}```'.format(result[0], result[2]) # 返答を生成

        await message.channel.send(answer)

    elif re.match(r'^!pdite', message.content): # プレシャスデイズプライズ表(物品)
        result = dice.d66table('table/PreciousDays/prize_item_table.csv')
        answer = '```プレシャスデイズ家名名前表 > {0} > {1}```'.format(result[0], result[2]) # 返答を生成

        await message.channel.send(answer)
    
    elif re.match(r'^!pdcha', message.content): # プレシャスデイズプライズ表(自身の変化)
        result = dice.d66table('table/PreciousDays/prize_change_table')
        answer = '```プレシャスデイズ家名名前表 > {0} > {1}```'.format(result[0], result[2]) # 返答を生成

        await message.channel.send(answer)

    elif re.match(r'^!pdfri', message.content): # プレシャスデイズプライズ表(友人)
        result = dice.d66table('table/PreciousDays/prize_friend_table')
        answer = '```プレシャスデイズ家名名前表 > {0} > {1}```'.format(result[0], result[2]) # 返答を生成

        await message.channel.send(answer)

    elif re.match(r'^!pdtec', message.content): # プレシャスデイズ師匠の呼び名表
        result = dice.d6table('table/PreciousDays/teacher_table.csv')
        answer = '```プレシャスデイズ師匠の呼び名表 > {0} > {1}```'.format(result[0], result[2]) # 返答を生成

        await message.channel.send(answer)

try:
    print('----------ADoCN botを実行しています----------')
    keep_alive()
    client.run(TOKEN, log_handler=handler)

except discord.errors.HTTPException as e:
    if e.status == 429: # Too Many Request
        print("---------- 429 Too Many Request : ADoCN botをSuspendします----------")
        suspend_render()
        time.sleep(60)

    else:
        raise e