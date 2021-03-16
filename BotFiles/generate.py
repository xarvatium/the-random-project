import wikipedia
import discord
import praw
from imgurpython import ImgurClient
from random import randint, choice
from discord.ext import commands
from googleapiclient.discovery import build  # Used for parsing YouTube API requests
from PIL import Image
import os
import requests
from urllib.error import HTTPError
import json  # Used for parsing the last.fm API responses
from time import time  # Used for getting the current time to avoid rate limiting
from pymongo import MongoClient
mongoclient = MongoClient('mongodb://localhost:27017')


def generate_config_reload():
    global config 
    with open('config.json') as configFile:
        config = json.load(configFile)


# def prefix(bot, message):
#     global client
#     if not message.guild:
#         return commands.when_mentioned_or("=")(bot, message)
#     mndb = mongoclient['the-random-bot']
#     posts = mndb['servers']
#     prefix = "="
#     for x in posts.find({"serverID": message.guild.id}):
#         prefix=x["prefix"]
#     return commands.when_mentioned_or(prefix)(bot, message)


bot = commands.Bot(command_prefix="%", help_command=None)


# Set a couple of variables that need to be global and persistent for random song
lastfm_update = 0
lastfm_tracklist = []


@bot.event  # Sets status on start and prints that it's logged in
async def on_ready():
    print('\nLogged in as {0.user}'.format(bot))
    await bot.change_presence(
        activity=discord.Game(
            name=";help || with dice"
        )
    )


@bot.command()
async def random(ctx):
    errorEmbed = discord.Embed(title="Oops!",
                               description='Did you mean to use ";generate"?',
                               color=0xB87DDF)
    await ctx.channel.send(embed=errorEmbed)


@bot.group()  # Defines the ;generate group with an error message if no argument is provided
async def generate(ctx):
    if ctx.invoked_subcommand is None:
        nullEmbed = discord.Embed(title="Error",
                                  description="Please include what to generate randomly. If you don't know what this is"
                                              ", use the ;help command!",
                                  color=0xC73333
                                  )
        await ctx.channel.send(embed=nullEmbed)


@generate.command()  # Random Wikipedia article Generator - Generates a random wikipedia article
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


@generate.command()  # Random Number Generator - Generates a random number
async def number(ctx, low: int = 0, high: int = 100):
    # The error it gives if there is no high or low
    numError = "There was an error! Did you make sure to give numbers and not words?"
    errorEmbed = discord.Embed(title="Error:",
                               description=numError,
                               color=0xB87DDF)
    try:
        ran = randint(low, high)
        numEmbed = discord.Embed(title="Random Number", description=ran, color=0xB87DDF)
        await ctx.channel.send(embed=numEmbed)
    except discord.Forbidden:
        await ctx.channel.send(embed=errorEmbed)


@generate.command()  # Random YouTube Video Generator - Gives a random YouTube video
async def video(ctx):
    import random
    global config
    # Defines the variables to be used
    youtubeApiServiceName = 'youtube'
    youtubeApiVersion = "v3"
    prefix = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
              'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    postfix = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    ]

    # This is what it uses to search
    def youtube_search():

        # Giving my API Key and Developer Key to Google's API
        youtube = build(youtubeApiServiceName, youtubeApiVersion, developerKey=config['ytApiKey'])

        # This is the actual code that searches YouTube and gives 5 results back, and chooses one
        searchResponse = youtube.search().list(
            q=random.choice(prefix) + str(random.randint(0, 9999)) + random.choice(postfix),
            part='snippet',
            maxResults=1
        ).execute()

        videos = []

        # This is the For statement that looks for actual YouTube videos and not just strings
        for search_result in searchResponse.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append('%s' % (search_result['id']['videoId']))
        return videos[random.randint(0, 0)]

    # The portion that is sent to Discord, with the base URL preceding the search results
    attempts = 0
    while attempts < 10:
        try:
            await ctx.channel.send("https://youtube.com/watch?v="+youtube_search())
            print("Sent YT video")
            break
        except IndexError:
            attempts += 1
            print("YouTube Error Caught, trying again")


@generate.command()  # Random Color Generator - Sends in embed and gives a file w/ HEX and RGB codes
async def color(ctx):
    # Defines the RGB to Hex function
    def rgb_to_hex(rgb):
        r, g, b = rgb
        return '#%02x%02x%02x' % (r, g, b)

    # This sets up the variables to be used
    colorRGB = (randint(0, 255), randint(0, 255), randint(0, 255))
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


@generate.command()  # Grabs a random song from last.fm
async def song(ctx, *, usertag=None):
    global lastfm_update  # This variable will be used to update old data without making multiple requests every time
    global lastfm_tracklist  # Will store the tracklist so it doesn't have to be called every time
    base_url = "http://ws.audioscrobbler.com/2.0/"
    if usertag:
        for s in ['&', '%', '+', '?', '=', '/']:
            usertag = usertag.replace(s, '')
    headers = {
        "user-agent": config['lastFmUA']
    }
    # Check if the last data update was over 3 hours ago
    if (time() - lastfm_update) > 10800:
        print('LFM Data expired!')
        lastfm_tracklist = {
            'taglist': [],
            'tags': {}
        }  # Empty lastfm tracklist with required data structure
        tagrq = requests.get(base_url + "?method=tag.getTopTags&format=json&api_key=" + config['lastFmKey'])
        tags = json.loads(tagrq.content.decode('UTF-8'))['toptags']['tag']  # Get the json response of tags into a list
        for tag in tags:
            lastfm_tracklist['tags'][tag['name']] = []  # Create an empty list for each tag
            lastfm_tracklist['taglist'].append(tag['name'])  # Append each tag to the taglist
        lastfm_update = time()  # Update the lastfm_update time
    if not usertag:  # If no tag is specified, get a random one instead
        usertag = choice(lastfm_tracklist['taglist'])
    elif usertag not in lastfm_tracklist['taglist']:  # If a usertag is defined but is not yet in the taglist, create a new list for the usertag and add it to the taglist
        trackrq = requests.get(base_url + "?method=tag.getTopTracks&format=json&tag=" + usertag.replace(' ', '%20') + "&api_key=" + config['lastFmKey'])  # Doing the webrequest here will let use check if it's a valid tag
        tracks = json.loads(trackrq.content.decode('UTF-8'))
        if tracks['tracks']['track'] != []:  # If the tracklist isn't empty (indicating a bad tag)
            lastfm_tracklist['taglist'].append(usertag)
            lastfm_tracklist['tags'][usertag] = tracks['tracks']['track']
    try:
        if lastfm_tracklist['tags'][usertag] == []:  # If it's an empty list
            trackrq = requests.get(base_url + "?method=tag.getTopTracks&format=json&tag=" + usertag.replace(' ', '%20') + "&api_key=" + config['lastFmKey'])  # Doing the webrequest here will let use check if it's a valid tag (again, but just to make sure there wasn't an issue)
            tracks = json.loads(trackrq.content.decode('UTF-8'))
            if tracks['tracks']['track'] != []:  # If the tracklist isn't empty (indicating a bad tag)
                lastfm_tracklist['tags'][usertag] = tracks['tracks']['track']
        track = choice(lastfm_tracklist['tags'][usertag])
        embed = discord.Embed(title=track['name'], color=0xB87DDF, url=track['url'])
        embed.add_field(name="Artist", value=track['artist']['name'])
        embed.add_field(name="Tag", value=usertag)
        embed.set_footer(text="Data provided by last.fm")
        await ctx.channel.send(embed=embed)
    except KeyError:
        await ctx.channel.send("Tag error! You may have specified an invalid tag for searching.")


@generate.command()  # Grabs a random randomizer
async def random(ctx):
    thingList = ['article', 'video', 'number', 'color', 'song']
    generator = choice(thingList)
    await ctx.channel.send("You get a random " + generator + "!")
    await globals()[generator](ctx)


@generate.command()
async def reddit(ctx, *, sub=None):
    r = praw.Reddit(
        client_id=config['reddit']['clientID'],
        client_secret=config['reddit']['clientSecret'],
        user_agent=config['reddit']['user_agent'],
        check_for_async=False
    )
    if not sub:
        subreddit = r.subreddit("all")
    elif sub:
        subreddit = r.subreddit(sub)

    try:
        submissions = [post for post in subreddit.hot(limit=200)]
    except discord.Forbidden:
        httpError = discord.Embed(title="Error",
                                  description="The sub requested is either locked or hidden, please try again.",
                                  color=0xC73333
                                  )
        await ctx.channel.send(embed=httpError)

    random_post_number = randint(0, 99)
    random_post = submissions[random_post_number]
    subTitle = random_post.title
    subAuth = random_post.author
    subDesc = random_post.selftext
    subLink = "https://www.reddit.com" + random_post.permalink
    subScore = random_post.score
    subUrl = random_post.url
    nsfw = random_post.over_18

    embedAuth = "/u/" + str(subAuth)
    embedScore = "Submission Score: " + str(subScore)

    redditEmbed = discord.Embed(title=subTitle, color=0xB87DDF)
    redditEmbed.set_author(name=embedAuth)
    redditEmbed.add_field(name="Post Link:", value=subLink)
    redditEmbed.set_image(url=subUrl)
    redditEmbed.set_footer(text=embedScore)


    if subDesc != "":
        redditEmbed.add_field(name="Description:", value=subDesc, inline=False)


    if nsfw:
        if ctx.channel.is_nsfw():
            await ctx.channel.send(embed=redditEmbed)
        elif not ctx.channel.is_nsfw():
            notNsfwEmbed = discord.Embed(title="Error:",
                                         description="Channel is not nsfw and the command pulled an nsfw post.",
                                         color=0xC73333)
            await ctx.channel.send(embed=notNsfwEmbed)
    else:
        await ctx.channel.send(embed=redditEmbed)


@generate.command()
async def image(ctx, *text: str):
    import random
    imgurID = config['imgur']['imgurID']
    imgurSecret = config['imgur']['imgurSecret']
    client = ImgurClient(imgurID, imgurSecret)
    rand = random.randint(0, 29)
    if text == ():
        searchEmbed = discord.Embed(title="Error:",
                                    description="Please enter a search term. (This does not support optional parameters)",
                                    color=0xC73333)
        await ctx.channel.send(embed=searchEmbed)
    elif text[0] != ():
        items = client.gallery_search(" ".join(text[0:len(text)]), advanced=None, sort='viral', window='all', page=0)
        try:
            imageRes = items[rand]
            await ctx.channel.send(imageRes.link)

        except IndexError:
            invalidError = discord.Embed(title="Error:",
                                         description="Sorry! I encountered an error somewhere along the way. (Did you include a __**valid**__ subreddit to search?)",
                                         color=0xC73333)
            await ctx.channel.send(embed=invalidError)
