import wikipedia, random, discord, time, tracemalloc, asyncio, json, os
from discord.ext import commands
from random import *
from dotenv import load_dotenv

client = commands.Bot(command_prefix=';', help_command=None)
tracemalloc.start()

def check_me(ctx):
    return ctx.message.author.id == 514866599400833034

randdict = {
    
}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="randomness unfold | ;"))

# @client.command()
# async def random_article(ctx):
    # wikipage = wikipedia.random(1)
    # wikiload = wikipedia.page(wikipage)
    # wikiEmbed = discord.Embed(title=wikipedia.page(wikipage).title, description=wikipedia.summary(wikipage), color=0xd1d1d1)
    # wikiEmbed.add_field(name="URL", value=wikiload.url, inline=False)
    # await ctx.channel.send(embed=wikiEmbed)
    # print("Sent Wiki Article")

@client.command()
async def help(ctx):
    helpEmbed = discord.Embed(title="Help", color=0xB87DDF)
    helpEmbed.add_field(name="Help", value="You're here right now lol")
    helpEmbed.add_field(name="random_article", value="Use this to generate a random article")
    await ctx.channel.send(embed=helpEmbed)

@client.group()
async def random(ctx):
    if ctx.invoked.subcommand is None:
        await ctx.send('Error: must include what to randomly generate.')

@random.command()
async def article(ctx):
        wikipage = wikipedia.random(1)
        wikiload = wikipedia.page(wikipage)
        wikiEmbed = discord.Embed(title=wikipedia.page(wikipage).title, description=wikipedia.summary(wikipage), color=0xB87DDF)
        wikiEmbed.add_field(name="URL", value=wikiload.url, inline=False)
        await ctx.channel.send(embed=wikiEmbed)
        print("Sent Wiki Article")
        
@random.command()
async def number(ctx, min = int, max = int):
    try:
        ran = randint(min, max)
        numEmbed = discord.Embed(title="Random Number", description=ran, color=0xB87DDF)
        await ctx.channel.send(embed=numEmbed)
    except:
        await ctx.channel.send("There was an error! Did you make sure you included a minimum/maximum?")

@client.command()
async def status(ctx, *args):
    if (ctx.message.author.id == 514866599400833034):
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=args))
    elif (ctx.message.author.id != 514866599400833034):
        await ctx.channel.send("Lol nice try nerd")
load_dotenv()
token = os.getenv('discord_token')
client.run(token)