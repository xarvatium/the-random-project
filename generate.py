import wikipedia
import discord
import youtube_dl
from random import *
from discord.ext import commands

client = commands.Bot(command_prefix=';', help_command=None)


@client.group()
async def generate(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.channel.send('Error: must include what to randomly generate.')


@generate.command()
async def article(ctx):
    wiki_page = wikipedia.random(1)
    wiki_load = wikipedia.page(wiki_page)
    wikiEmbed = discord.Embed(title=wikipedia.page(wiki_page).title,
                              description=wikipedia.summary(wiki_page),
                              color=0xB87DDF)
    wikiEmbed.add_field(name="URL", value=wiki_load.url, inline=False)
    try:
        await ctx.channel.send(embed=wikiEmbed)
        print("Sent Wiki Article")
    except discord.Forbidden:
        await ctx.channel.send("The article you requested had a disambiguation, please try again.")


@generate.command()
async def number(ctx, low: int, high: int):
    numError = "There was an error! Did you make sure you included a minimum/maximum or to give numbers and not words?"
    errorEmbed = discord.Embed(title="Error:",
                               description=numError,
                               color=0xB87DDF)
    try:
        ran = randint(low, high)
        numEmbed = discord.Embed(title="Random Number", description=ran, color=0xB87DDF)
        await ctx.channel.send(embed=numEmbed)
    except discord.Forbidden:
        await ctx.channel.send(embed=errorEmbed)


@generate.command()
async def video(ctx):
    import random
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

    characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d",
                  "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                  "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                  "y", "z", "-", "_"]
    result = ""
    for i in range(0, 11):
        result += random.choice(characters)
    print(result)
    with ydl:
        result2 = ydl.extract_info(
            'http://youtube.com/watch?v=' + result,
            download=False
        )
    if 'entries' in result2:
        videoOut = result2['entries'][0]
    else:
        videoOut = result2
    print(videoOut)
    video_url = video['url']
    await ctx.channel.send(video_url)
