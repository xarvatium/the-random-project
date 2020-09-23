import wikipedia, random, discord, time, tracemalloc, asyncio, json, os
from discord.ext import commands
from random import *
from dotenv import load_dotenv

client = commands.Bot(command_prefix=';', help_command=None)
tracemalloc.start()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="randomness unfold | ;"))

@client.command()
async def help(ctx):
    helpEmbed = discord.Embed(title="Help", color=0xB87DDF)
    helpEmbed.add_field(name="Help", value="You're here right now lol")
    helpEmbed.add_field(name="random_article", value="Use this to generate a random article")
    await ctx.channel.send(embed=helpEmbed)

@client.group()
async def random(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.channel.send('Error: must include what to randomly generate.')

@random.command()
async def article(ctx):
        wiki_page = wikipedia.random(1)
        wiki_load = wikipedia.page(wiki_page)
        wikiEmbed = discord.Embed(title=wikipedia.page(wiki_page).title, description=wikipedia.summary(wiki_page), color=0xB87DDF)
        wikiEmbed.add_field(name="URL", value=wiki_load.url, inline=False)
        await ctx.channel.send(embed=wikiEmbed)
        print("Sent Wiki Article")
        
@random.command()
async def number(ctx, min: int, max: int):
    errorEmbed = discord.Embed(title="Error:", description="There was an error! Did you make sure you included a minimum/maximum or to give numbers and not words?", color=0xB87DDF)
    try:
        ran = randint(min, max)
        numEmbed = discord.Embed(title="Random Number", description=ran, color=0xB87DDF)
        await ctx.channel.send(embed=numEmbed)
    except discord.Forbidden:
        await ctx.channel.send(embed=errorEmbed)

@client.command()
async def status(ctx, arg):
    import developers
    dev_list = developers.dev_list["Developers"]["User IDs"]
    if (ctx.message.author.id in dev_list):
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=arg))

    else:
        await ctx.channel.send("Placeholder")

# The Token initialization
load_dotenv()
token = os.getenv('discord_token')
client.run(token)