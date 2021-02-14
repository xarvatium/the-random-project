import wikipedia
import discord
from random import *
from discord.ext import commands
from googleapiclient.discovery import build
from PIL import Image
from keys import *
import os
import requests

bot = commands.Bot(command_prefix=';', help_command=None)

# Gives the even that tells the bot is up, also sets the status
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="In Maintenance | ;"
        )
    )


# Sets the "generate" group for the ;generate <command> group
@bot.group()
async def generate(ctx):
    if ctx.invoked_subcommand is None:
        nullEmbed = discord.Embed(title="Error", description="Please include what to generate randomly. If you don't know what this is, use the ;help command!", color=0xB87DDF)
        await ctx.channel.send(embed=nullEmbed)


# Generates a random Wikipedia article
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


# Generates a random number between the <low> and the <high> given by the user
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


# Generates a random YouTube video
@generate.command()
async def video(ctx):
    import random

    # Defines the variables to be used
    youtubeApiServiceName = 'youtube'
    youtubeApiVersion = "v3"
    prefix = ['IMG ', 'IMG_', 'IMG-', 'DSC ']
    postfix = [' MOV', '.MOV', ' .MOV']

    # This is what it uses to search
    def youtube_search():

        # Giving my API Key and Developer Key to Google's API
        youtube = build(youtubeApiServiceName, youtubeApiVersion, developerKey=DEVELOPER_KEY)

        # This is the actual code that searches YouTube and gives 5 results back, and chooses one
        searchResponse = youtube.search().list(
            q=random.choice(prefix) + str(random.randint(999, 9999)) + random.choice(postfix),
            part='snippet',
            maxResults=5
        ).execute()

        videos = []

        # This is the For statement that looks for actual YouTube videos and not just strings that fit Google's naming scheme
        for search_result in searchResponse.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append('%s' % (search_result['id']['videoId']))
        return videos[random.randint(0, 2)]

    # The portion that is sent to Discord, with the base URL preceding the search results
    await ctx.channel.send("https://youtube.com/watch?v="+youtube_search())
    print("Sent YT video")


# Gives a random color sent in an embed and a file
@generate.command()
async def color(ctx):
    # Defines the RGB to Hex function
    def rgb_to_hex(rgb):
        r,g,b = rgb
        return '#%02x%02x%02x' % (r,g,b)

    # This sets up the variables to be used
    colorRGB = (randint(0,255), randint(0,255), randint(0,255))
    colorHex = rgb_to_hex(colorRGB)
    colorDesc = "Hex Code: " + "**" + colorHex + "**" + "\n" + "RGB Code: " + "**" + str(colorRGB) + "**"
    width = 128
    height = 128

    # Creates an image and saves it then puts it into a Discord embed
    img = Image.new(
        mode="RGB",
        size=(width, height),
        color=colorRGB
    )
    img.save("color.png")
    file = discord.File("color.png")
    colorEmbed = discord.Embed(
        title="Your Color is:",
        description=colorDesc,
        color=0xB87DDF
    )
    # What is actually sent to Discord
    colorEmbed.set_image(url="attachment://color.png")
    await ctx.channel.send(file=file, embed=colorEmbed)
    print("Sent image")
    os.remove("color.png")
