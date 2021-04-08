import json  # Used for parsing the last.fm API responses
import os  # Used to find specific files in various different commands
from random import randint, choice  # Used for the homebrew generators
from time import time  # Used for getting the current time to avoid rate limiting

import discord  # Used for Discord's API
import numpy as np
import praw  # Used to parse Reddit data
import requests  #
import wikipedia  # Used for the Wikipedia API
from PIL import Image  # Pillow, used for the image generator in ;generate color
from PyDictionary import PyDictionary
from discord.ext import commands  # Used to have commands in the bot
from googleapiclient.discovery import build  # Used for parsing YouTube API requests
from imgurpython import ImgurClient  # Used for Imgur's API
from pymongo import MongoClient
from random_word import RandomWords
from youtube_search import YoutubeSearch

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


bot = commands.Bot(command_prefix=";", help_command=None)


# Set a couple of variables that need to be global and persistent for random song
lastfm_update = 0
lastfm_tracklist = []

# Random Word global variables
randomWordUpdate = 0


@bot.event  # Sets status on start and prints that it's logged in
async def on_ready():
    print('\nLogged in as {0.user}'.format(bot))
    await bot.change_presence(
        activity=discord.Game(
            name=";help || v1.5 POG"
        )
    )


@bot.command()  # Making sure the users don't do ;random instead of ;generate
async def random(ctx):
    errorEmbed = discord.Embed(title="Oops!",
                               description='Did you mean to use ";generate"?',
                               color=0xB87DDF)
    await ctx.channel.send(embed=errorEmbed)


@bot.group()  # Defines the ;generate group with an error message if no argument is provided
async def generate(ctx):
    if ctx.invoked_subcommand is None:  # Checking if a subcommand is being called
        nullEmbed = discord.Embed(title="Error",
                                  description="Please include what to generate randomly. If you don't know what this is"
                                              ", use the ;help command!",
                                  color=0xC73333
                                  )
        await ctx.channel.send(embed=nullEmbed)  # Sends the error if there is no subcommand provided


@generate.command()  # Random Wikipedia article Generator - Generates a random wikipedia article
async def article(ctx):
    # Defining variables
    wikiPage = wikipedia.random(1)
    wikiLoad = wikipedia.page(wikiPage)
    wikiEmbed = discord.Embed(title=wikipedia.page(wikiPage).title,
                              description=wikipedia.summary(wikiPage),
                              color=0xB87DDF)
    # Adding a field with the URL to the embed
    wikiEmbed.add_field(name="URL", value=wikiLoad.url, inline=False)
    try:
        await ctx.channel.send(embed=wikiEmbed)
        print("Sent Wiki Article")
    except:
        errorEmbed = discord.Embed(title="Error:",
                                   description="It appears the page I found doesn't exist, please try again.")
        await ctx.channel.send(embed=errorEmbed)


@generate.command()  # Random Number Generator - Generates a random number
async def number(ctx, low: int = 0, high: int = 100, type=None):
    if low > high: low, high = high, low
    # The error it gives if there is no high or low
    numError = "There was an error! Did you make sure to give numbers and not words?"
    errorEmbed = discord.Embed(title="Error:",
                               description=numError,
                               color=0xC73333)
    ran = randint(low, high)
    numEmbed = discord.Embed(title=f"Your Random Number Between {low} and {high} is", description=ran, color=0xB87DDF)
    if type is None:
        try:
            await ctx.channel.send(embed=numEmbed)
        except discord.Forbidden:
            await ctx.channel.send(embed=errorEmbed)
    elif type.lower() == "prime":
        def getRandomPrimeInteger(bounds):

            for i in range(bounds.__len__() - 1):
                if bounds[i + 1] > bounds[i]:
                    x = bounds[i] + np.random.randint(bounds[i + 1] - bounds[i])
                    if isPrime(x):
                        return x

                else:
                    if isPrime(bounds[i]):
                        return bounds[i]

                if isPrime(bounds[i + 1]):
                    return bounds[i + 1]

            newBounds = [0 for i in range(2 * bounds.__len__() - 1)]
            newBounds[0] = bounds[0]
            for i in range(1, bounds.__len__()):
                newBounds[2 * i - 1] = int((bounds[i - 1] + bounds[i]) / 2)
                newBounds[2 * i] = bounds[i]

            return getRandomPrimeInteger(newBounds)

        def isPrime(x):
            count = 0
            for i in range(int(x / 2)):
                if x % (i + 1) == 0:
                    count = count + 1
            return count == 1

        bounds = [low, high]
        # Gets 1 prime number from the range
        for i in range(1):
            boundsError = discord.Embed(title="Bounds Error",
                                        description="Sorry, it appears I was not made to handle your cryptographical needs. Please try a high and low below 2^20",
                                        color=0xC73333
                                        )
            if low >= 1048576 or high >= 1048576:
                await ctx.channel.send(embed=boundsError)
                break
            x = getRandomPrimeInteger(bounds)
            primeEmbed = discord.Embed(title="Random Prime Number",
                                       description=x,
                                       color=0xB87DDF
                                       )
            await ctx.channel.send(embed=primeEmbed)

    elif type.lower() == "odd":
        odd = ran % 2
        if odd == 1:
            oddEmbed = discord.Embed(title="Random Odd Number", description=ran, color=0xB87DDF)
            await ctx.channel.send(embed=oddEmbed)

        else:
            ran += 1
            oddEmbed = discord.Embed(title="Random Odd Number", description=ran, color=0xB87DDF)
            await ctx.channel.send(embed=oddEmbed)
    elif type.lower() == "even":
        even = ran % 2
        if even == 0:
            evenEmbed = discord.Embed(title="Random Even Number", description=ran, color=0xB87DDF)
            await ctx.channel.send(embed=evenEmbed)
        else:
            ran += 1
            evenEmbed = discord.Embed(title="Random Even Number", description=ran, color=0xB87DDF)
            await ctx.channel.send(embed=evenEmbed)



@generate.command()  # Random YouTube Video Generator - Gives a random YouTube video
async def video(ctx):
    import random
    # Defines the variables to be used
    prefix = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
              'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    postfix = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    ]

    # The portion that is sent to Discord, with the base URL preceding the search results
    attempts = 0
    while attempts < 10:  # Due to a strange error, I have it set to iterate 10 times until it succeeds
        try:
            videos = YoutubeSearch(random.choice(prefix) + str(random.randint(0, 9999)) + random.choice(postfix),
                                   max_results=10,
                                   ).to_dict()
            ranVid = random.choice(videos)
            ytLink = "https://www.youtube.com/watch?v=" + ranVid['id']
            await ctx.channel.send(ytLink)
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

    randomPostNumber = randint(0, 99)
    randomPost = submissions[randomPostNumber]
    subTitle = randomPost.title
    subAuth = randomPost.author
    subDesc = randomPost.selftext
    subLink = "https://www.reddit.com" + randomPost.permalink
    subScore = randomPost.score
    subUrl = randomPost.url
    nsfw = randomPost.over_18

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


@generate.command()
async def word(ctx):
    dictionary = PyDictionary()

    while True:
        try:
            ranWord = RandomWords()
            word = ranWord.get_random_word(hasDictionaryDef="true")
            print(word)
            meaning = dictionary.meaning(word)
            synonyms = dictionary.synonym(word)
            antonyms = dictionary.antonym(word)

            break
        except Exception:
            pass

    cleanMeaning = str(meaning).replace('{', '').replace('[', '').replace(']', '').replace('}', '').replace("'", '')
    cleanSyns = str(synonyms).replace('[', '').replace(']', '').replace("'", '')
    cleanAnt = str(antonyms).replace('[', '').replace(']', '').replace("'", '')

    wordEmbed = discord.Embed(title=f"Random Word - {word.capitalize()}",
                              description=f"{cleanMeaning}\n",
                              color=0xB87DDF)
    wordEmbed.add_field(name="Synonyms",
                        value=cleanSyns)
    wordEmbed.add_field(name="Antonyms",
                        value=cleanAnt)
    await ctx.channel.send(embed=wordEmbed)
