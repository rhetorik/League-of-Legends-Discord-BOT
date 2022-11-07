import string
from riotwatcher import LolWatcher, ApiError
import discord
from discord.ext import commands, tasks
import os
import json


intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix="@", intents=intents) 

key = "RGAPI-3234c296-5a09-4b7a-b1e8-7694d2be082f"
watcher = LolWatcher(key)
platform_routing_value = "NA1"

QUEUE_ID_DICT = {4: 'RANKED', 6: 'RANKED', 42: 'RANKED', 420: 'RANKED', 65: 'ARAM', 100: 'ARAM', 450: 'ARAM', 0: 'CUSTOM', 440: 'FLEX', 700: 'CLASH'}

CHAMP_DICT = {103: 'Ahri', 84: 'Akali', 166: 'Akshan', 12: 'Alistar', 32: 'Amumu', 34: 'Anivia', 1: 'Annie', 22: 'Ashe', 136: 'AurelionSol', 200: 'Belveth', 53: 'Blitzcrank', 63: 'Brand', 201: 'Braum', 51: 'Caitlyn', 164: 'Camille', 69: 'Cassiopeia', 31: 'Chogath', 42: 'Corki', 122: 'Darius', 131: 'Diana', 119: 'Draven', 36: 'DrMundo', 245: 'Ekko', 60: 'Elise', 28: 'Evelynn', 81: 'Ezreal', 9: 'Fiddlesticks', 114: 'Fiora', 105: 'Fizz', 3: 'Galio', 41: 'Gangplank', 86: 'Garen', 150: 'Gnar', 79: 'Gragas', 104: 'Graves', 120: 'Hecarim', 74: 'Heimerdinger', 39: 'Irelia', 40: 'Janna', 59: 'JarvanIV', 24: 'Jax', 126: 'Jayce', 202: 'Jhin', 222: 'Jinx', 145: 'Kaisa', 43: 'Karma', 30: 'Karthus', 38: 'Kassadin', 55: 'Katarina', 10: 'Kayle', 141: 'Kayn', 85: 'Kennen', 121: 'Khazix', 203: 'Kindred', 240: 'Kled', 96: 'KogMaw', 7: 'Leblanc', 64: 'LeeSin', 89: 'Leona', 127: 'Lissandra', 236: 'Lucian', 117: 'Lulu', 99: 'Lux', 54: 'Malphite', 90: 'Malzahar', 57: 'Maokai', 11: 'MasterYi', 21: 'MissFortune', 62: 'MonkeyKing', 82: 'Mordekaiser', 25: 'Morgana', 75: 'Nasus', 111: 'Nautilus', 76: 'Nidalee', 56: 'Nocturne', 20: 'Nunu', 2: 'Olaf', 61: 'Orianna', 80: 'Pantheon', 78: 'Poppy', 246: 'Qiyana', 133: 'Quinn', 33: 'Rammus', 58: 'Renekton', 107: 'Rengar', 92: 'Riven', 68: 'Rumble', 13: 'Ryze', 113: 'Sejuani', 235: 'Senna', 147: 'Seraphine', 35: 'Shaco', 98: 'Shen', 102: 'Shyvana', 27: 'Singed', 14: 'Sion', 15: 'Sivir', 72: 'Skarner', 37: 'Sona', 16: 'Soraka', 50: 'Swain', 134: 'Syndra', 223: 'TahmKench', 163: 'Taliyah', 91: 'Talon', 44: 'Taric', 17: 'Teemo', 18: 'Tristana', 48: 'Trundle', 23: 'Tryndamere', 4: 'TwistedFate', 29: 'Twitch', 77: 'Udyr', 6: 'Urgot', 110: 'Varus', 67: 'Vayne', 45: 'Veigar', 161: 'Velkoz', 234: 'Viego', 112: 'Viktor', 8: 'Vladimir', 106: 'Volibear', 19: 'Warwick', 101: 'Xerath', 5: 'XinZhao', 157: 'Yasuo', 83: 'Yorick', 154: 'Zac', 238: 'Zed', 221: 'Zeri', 115: 'Ziggs', 26: 'Zilean', 142: 'Zoe', 143: 'Zyra', 266: 'Aatrox', 523: 'Aphelios', 268: 'Azir', 432: 'Bard', 887: 'Gwen', 420: 'Illaoi', 427: 'Ivern', 429: 'Kalista', 876: 'Lillia', 267: 'Nami', 518: 'Neeko', 895: 'Nilah', 516: 'Ornn', 555: 'Pyke', 497: 'Rakan', 421: 'RekSai', 526: 'Rell', 888: 'Renata', 360: 'Samira', 875: 'Sett', 517: 'Sylas', 412: 'Thresh', 711: 'Vex', 254: 'Vi', 498: 'Xayah', 777: 'Yone', 350: 'Yuumi'}

f = open("champion.json", encoding="utf-8")
champs = json.load(f)


def find_champ(champs, code):
    names = list(champs["data"].keys())
    for i in names:
        if int(champs["data"][i]["key"]) == code:
            return i

@bot.event
async def on_ready():
    print("Bot is running as {0.user}".format(bot))

@bot.command(name="search")
async def search_summoner(ctx, *, summoner):
    try:
        summ_data = watcher.summoner.by_name(platform_routing_value, summoner)
        ranked_stats = watcher.league.by_summoner("na1", summ_data['id'])
        print(summ_data)
        SOLO_QUEUE = ranked_stats[0] if ranked_stats[0]['queueType'] == 'RANKED_SOLO_5x5' else ranked_stats[1]
        sum_lookup = discord.Embed(description="LEVEL: " + str(summ_data["summonerLevel"]) + "\n"
                        "RANK: " + SOLO_QUEUE['tier'] + " " + SOLO_QUEUE['rank'] + " " + str(SOLO_QUEUE['leaguePoints']) + "LP" + "\n"
                       "GAMES: " + str(SOLO_QUEUE['wins'] + SOLO_QUEUE['losses']) + "\n"
                       "WINS: " + str(SOLO_QUEUE['wins']) + "      " + "LOSSES: " + str(SOLO_QUEUE['losses']) + "\n"
                       "W/R: " + str(round(SOLO_QUEUE['wins'] / SOLO_QUEUE['losses'], 2)))
        prof_icon = discord.File("refs/profileicon/" + str(summ_data["profileIconId"]) + ".png", filename="image.png")
        sum_lookup.set_author(name= summ_data["name"], icon_url="attachment://image.png")
        await ctx.send(file=prof_icon, embed=sum_lookup)
        
    except ApiError as err:
        if err.response.status_code == 404:
            await ctx.send("summoner does not exist")
        
        
# @bot.command(name="champs")
# async def champs_and_keys(ctx, * , summoner):
#     names = list(champs["data"].keys())
#     output = ""
#     for i in names:
#         for j in range(250, 1000):
#             if int(champs["data"][i]["key"]) == j:
#                 output += str(j) + ": " + """'""" + i + """'""" + ", "
#     await ctx.send(output)
        
@bot.command(name="current")
async def current_game(ctx, *, summoner):
    try:
        blue = "BLUE TEAM\n"
        red = "RED TEAM\n"
        summ_data = watcher.summoner.by_name(platform_routing_value, summoner)
        sum_id = summ_data["id"]
        cur_match = watcher.spectator.by_summoner(platform_routing_value, sum_id)
        print(cur_match)
        index = cur_match["participants"]
        for i in index:
            if i['teamId'] == 100:
                blue += i["summonerName"] + " - " + CHAMP_DICT[i["championId"]] + "\n"
            else:
                red += i["summonerName"] + " - " + CHAMP_DICT[i["championId"]] + "\n"
        await ctx.send(blue)
        await ctx.send(red)
        
    except ApiError as err:
        if err.response.status_code == 404:
            await ctx.send("summoner does not exist")

bot.run("MTAyMzA3NTA3NTYzMDU3OTgxNA.GX2u8g.4ekDvPiDOYBErGR6bE3wILRlNpzij-do5DMPd0")



