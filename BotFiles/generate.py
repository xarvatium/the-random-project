import json  # Used for parsing the last.fm API responses
import os  # Used to find specific files in various different commands
from random import randint, choice  # Used for the homebrew generators
import time  # Used for getting the current time to avoid rate limiting

import discord  # Used for Discord's API
import numpy as np
import praw  # Used to parse Reddit data
import requests  #
import wikipedia  # Used for the Wikipedia API
from PIL import Image  # Pillow, used for the image generator in ;generate color
from PyDictionary import PyDictionary
from discord.ext import commands  # Used to have commands in the bot
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


@bot.group()
async def encode(ctx):
    if ctx.invoked_subcommand is None:  # Checking if a subcommand is being called
        nullEmbed = discord.Embed(title="Error",
                                  description="Please include what to encode. If you don't know what this is"
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
    if (time.time() - lastfm_update) > 10800:
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
        lastfm_update = time.time()  # Update the lastfm_update time
    if not usertag:  # If no tag is specified, get a random one instead
        usertag = choice(lastfm_tracklist['taglist'])
    elif usertag not in lastfm_tracklist[
        'taglist']:  # If a usertag is defined but is not yet in the taglist, create a new list for the usertag and add it to the taglist
        trackrq = requests.get(
            base_url + "?method=tag.getTopTracks&format=json&tag=" + usertag.replace(' ', '%20') + "&api_key=" + config[
                'lastFmKey'])  # Doing the webrequest here will let use check if it's a valid tag
        tracks = json.loads(trackrq.content.decode('UTF-8'))
        if tracks['tracks']['track'] != []:  # If the tracklist isn't empty (indicating a bad tag)
            lastfm_tracklist['taglist'].append(usertag)
            lastfm_tracklist['tags'][usertag] = tracks['tracks']['track']
    try:
        if lastfm_tracklist['tags'][usertag] == []:  # If it's an empty list
            trackrq = requests.get(
                base_url + "?method=tag.getTopTracks&format=json&tag=" + usertag.replace(' ', '%20') + "&api_key=" +
                config[
                    'lastFmKey'])  # Doing the webrequest here will let use check if it's a valid tag (again, but just to make sure there wasn't an issue)
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


def deobfuscate(phrase, push1, push2, push2Interval, push3, push3Interval):
    iteration = 0
    deMathed = []
    clearString = ""
    for char in phrase.split('/'):
        char = int(char) - push1
        if (iteration % push2Interval) == 0:
            char -= push2
        if (iteration % push3Interval) == 0:
            char -= push3
        deMathed.append(char)
        iteration += 1
    for char in deMathed:
        clearString += chr(int(char))
    return (clearString)


@generate.command()
async def fact(ctx):
    chance = randint(1, 1)
    if chance == 1:
        message1 = await ctx.channel.send(deobfuscate(
            "509/443/435/423/436/483/358/394/437/358/558/437/443/358/430/538/423/440/358/435/558/358/435/427/441/552/423/429/427/389",
            189, 137, 1, 111, 5))
        time.sleep(2)
        message2 = await ctx.channel.send(deobfuscate(
            "553/249/409/311/323/497/392/311/401/242/596/324/412/315/401/502/323/326/402/242/583/311/407/242/396/509/323/309/402/320/596/307/390/326/323/518/396/326/395/242/601/321/408/256",
            210, 81, 2, 189, 5))
        time.sleep(2)
        message3 = await ctx.channel.send(deobfuscate(
            "597/282/369/588/398/282/603/364/394/594/364/347/633/359/351/591/315/366/602/282/395/605/361/368/629/350/351/537/315/334/602/282/386/596/368/351/556/351/347/590/387/282/603/351/397/606/361/360/556/366/354/592/315/365/588/366/388/606/352/347/623/366/355/602/393/282/602/352/315/599/351/347/638/360/355/601/386/282/601/351/402/523/355/360/640/351/364/592/398/366/596/360/386/523/366/354/629/360/353/606/315/347/607/282/397/588/360/350/635/359/296",
            250, 33, 4, 241, 3))
        time.sleep(3)
        message4 = await ctx.channel.send(deobfuscate(
            "537/464/462/555/469/457/559/463/456/486/457/450/569/385/456/565/463/454/486/450/472/568/474/399/486/418/469/486/468/464/563/454/385/566/464/458/564/469/397/486/426/392/572/454/385/552/454/456/551/463/385/570/464/385/562/454/450/568/463/385/556/467/464/563/385/469/558/454/468/555/385/455/551/452/469/569/399",
            157, 196, 1, 101, 3))
        time.sleep(2)
        message5 = await ctx.channel.send(deobfuscate(
            "540/358/506/357/499/357/583/347/575/350/499/339/499/350/572/358/583/350/568/274/571/339/589/363/511/274/565/359/583/274/540/281/585/343/499/344/578/356/576/343/567/274/564/274/566/353/576/354/575/343/583/343/499/351/578/342/568/350/499/353/569/274/571/359/576/339/577/274/582/353/566/347/568/358/588/288/499/311/585/343/581/363/499/339/566/358/572/353/577/274/578/344/499/343/585/343/581/363/499/354/568/356/582/353/577/274/566/339/577/274/565/343/499/354/568/356/569/343/566/358/575/363/499/341/564/350/566/359/575/339/583/343/567/288",
            242, 171, 2, 54, 2))
        time.sleep(4)
        message6 = await ctx.channel.send(deobfuscate(
            "467/383/391/458/304/353/512/377/388/496/304/387/500/381/384/503/373/318/427/346/389/510/388/304/503/383/383/502/304/369/511/304/376/506/391/304/511/376/377/505/375/387/427/387/388/492/386/388/496/372/316/427/369/384/507/380/393/427/369/304/503/377/388/511/380/373/427/385/389/492/382/388/512/381/304/494/369/380/494/389/380/492/388/377/506/382/316/427/369/382/495/304/370/492/381/316/427/369/304/507/373/386/497/373/371/511/304/387/500/381/389/503/369/388/500/383/382/441/304",
            116, 123, 3, 156, 1))
        time.sleep(3)
        message7 = await ctx.channel.send(deobfuscate(
            "332/296/297/307/280/304/293/306/350/293/291/308/280/307/297/301/365/300/289/308/353/303/302/224/352/289/307/224/356/293/292/224/357/293/224/308/359/224/303/302/349/224/294/289/347/308/250/224/353/302/224/303/362/292/293/306/280/308/303/224/345/291/291/303/357/304/300/297/363/296/224/301/369/224/295/303/345/300/224/303/350/224/304/306/359/310/297/292/353/302/295/224/362/289/302/292/359/301/302/293/363/307/224/308/359/224/308/296/349/224/311/303/362/300/292/236/280/265/224/301/365/307/308/224/362/293/307/296/345/304/293/224/363/303/291/297/349/308/313/224/345/306/303/309/358/292/224/308/362/309/293/224/362/289/302/292/359/301/302/293/363/307/238",
            70, 122, 1, 56, 4))
        time.sleep(4.5)
        message8 = await ctx.channel.send(deobfuscate(
            "228/145/150/139/169/149/113/72/172/137/235/141/100/155/157/216/172/72/137/72/257/141/154/142/169/216/156/72/183/145/226/157/176/137/156/222/179/150/84/72/218/72/147/150/179/236/72/156/172/137/233/72/189/151/157/156/186/141/72/155/246/141/150/72/184/221/145/155/100/149/218/155/183/137/143/218/114/72/105/150/245/72/113/72/175/227/151/159/100/159/221/137/184/72/161/228/185/79/148/148/177/140/151/72/178/218/160/156/114",
            40, 77, 5, 28, 4))
        time.sleep(3)
        message9 = await ctx.channel.send(deobfuscate(
            "517/189/406/412/410/276/476/276/403/413/331/276/549/265/407/334/403/258/552/269/331/411/400/201/476/254/409/402/331/276/548/268/331/421/404/265/552/189/414/418/410/269/476/266/400/348/331/241/548/268/414/403/331/276/548/268/331/418/413/278/476/273/410/334/414/273/555/269/331/411/400/189/563/262/407/410/331/272/561/259/401/403/413/189/563/271/396/418/403/189/563/261/400/412/331/266/565/189/400/422/404/272/560/258/409/401/400/189/549/272/331/416/400/254/552/262/421/403/399/203/476",
            157, 145, 3, 142, 2))
        time.sleep(3)
        message10 = await ctx.channel.send(deobfuscate(
            "407/165/115/86/443/159/187/158/356/170/175/159/439/86/178/164/435/173/179/155/424/157/172/98/356/173/176/162/432/86/192/165/441/86/175/155/432/166/103/152/438/159/181/157/356/163/172/86/429/164/187/165/356/155/191/159/439/170/172/164/423/155/134/86/403/168/103/173/429/162/179/86/445/165/188/86/422/155/103/170/428/155/103/168/425/153/172/159/442/155/185/86/435/156/103/163/445/86/190/168/421/170/175/117/356/127/103/161/434/165/190/86/443/158/168/170/356/175/182/171/363/162/179/86/424/165/117/86/395/165/103/151/428/155/168/154/356/151/181/154/356/171/186/155/356/175/182/171/438/86/173/151/431/155/103/156/438/155/172/86/443/159/179/162/356/170/182/86/358/154/172/153/429/154/172/88/370",
            54, 253, 4, 17, 2))
        time.sleep(5)
        message11 = await ctx.channel.send(deobfuscate(
            "500/128/335/327/342/49/533/128/253/312/338/133/449/133/325/318/336/49/532/121/332/327/337/61/449/115/338/329/253/90/449/133/325/318/331/124/449/59/337/317/322/138/456/135/322/255/253/127/528/133/326/312/322/117/463",
            17, 196, 3, 204, 2))
        time.sleep(1)
        message12 = await ctx.channel.send(deobfuscate(
            "485/172/254/199/257/465/220/196/267/209/523/174/220/197/267/462/268/215/272/203/521/201/220/212/253/463/256/209/265/162/513/195/255/214/230/427",
            130, 58, 2, 255, 5))
        time.sleep(1)
        response = json.loads(requests.get("https://uselessfacts.jsph.pl/random.json?language=en").text)
        factEmbed = discord.Embed(title="Your Fact:",
                                  description=response['text'],
                                  color=0xB87DDF)
        factEmbed.set_footer(text=f"Source - {response['source']}")
        await ctx.channel.send(embed=factEmbed)
        time.sleep(7)
        await message1.delete()
        await message2.delete()
        await message3.delete()
        await message4.delete()
        time.sleep(3)
        await message5.delete()
        await message6.delete()
        await message7.delete()
        await message8.delete()
        time.sleep(2)
        await message9.delete()
        await message10.delete()
        await message11.delete()
        await message12.delete()
    else:
        response = json.loads(requests.get("https://uselessfacts.jsph.pl/random.json?language=en").text)
        factEmbed = discord.Embed(title="Your Fact:",
                                  description=response['text'],
                                  color=0xB87DDF)
        factEmbed.set_footer(text=f"Source - {response['source']}")
        await ctx.channel.send(embed=factEmbed)

