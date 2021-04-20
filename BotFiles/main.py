import asyncio
from generate import *
from pymongo import MongoClient
import decimal
mongoclient = MongoClient('mongodb://localhost:27017')


# test

# Having helpText assigned here will cause helptext to only get read once, reducing disk access
helpText = {}
with open('helpText') as helpFile:
    helpString = helpFile.read()
helpText['general'] = helpString.split("<general>\n")[1].split("\n</general>")[0]
helpText['random1'] = helpString.split("<random1>\n")[1].split("\n</random1>")[0]
helpText['random2'] = helpString.split("<random2>\n")[1].split("\n</random2>")[0]

@bot.event  # When the bot joins a guild, it adds the default prefix and server ID to a database table
async def on_guild_join(guild):  # Logs when the bot joins a guild (does not log ID, so don't worry)
    # Defining variables
    mndb = mongoclient['the-random-bot']
    servercol = mndb['servers']
    serverID = guild.id
    serverName = guild.name
    serverDict = { 'serverID': serverID, "serverName": serverName, "prefix": ";" }
    dbWrite = servercol.insert_one(serverDict)
    channel = bot.get_channel(811010228945682432)
    joinDesc = "Server ID: " + str(serverID) + "\nServer Name: " + str(serverName) + "\nDatabase Result: " + str(dbWrite)
    joinServerEmbed = discord.Embed(title="Added to a new server!", description=joinDesc)
    await channel.send(embed=joinServerEmbed)


# \/ General Commands \/
@bot.command()  # The help command
async def help(ctx):
    helpEmbed = discord.Embed(title="Help Page",
                              description="__Bot Prefix is: **;**__\n**<>** - optional tag\n**[]** - required tag",  #.format(prefix)
                              color=0xB87DDF
                              )  # Defines the main portion of the help embed
    helpEmbed.add_field(name="General Commands",
                        value=helpText['general'],
                        inline=False
                        )  # Defines the General Commands category
    helpEmbed.add_field(name="\_\_\_\_\_\_\_Random Generator Commands\_\_\_\_\_\_\_",
                        value=helpText['random1'],
                        inline=True
                        )  # Defines the random portion of the section
    helpEmbed.add_field(name="\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_",
                        value=helpText['random2'],
                        inline=True
                        )  # Defines the random portion of the section
    helpEmbed.add_field(name="Support",
                        value="If you need support, please join the [Development Server](https://discord.gg/3hry5EFuM4) or head over to the GitHub page and open an [issue](https://github.com/xarvatium/the-random-project/issues).",
                        inline=False
                        )
    helpEmbed.set_footer(text="Creator: Xarvatium#6561",
                         icon_url="https://cdn.discordapp.com/avatars/514866599400833034/afa0052cc224e2d4135d565b564ff5d8.png?size=128"
                         )
    helpEmbed.set_author(name="The Random Bot", url="https://github.com/xarvatium/the-random-project", icon_url="https://cdn.discordapp.com/avatars/755986454907191319/39f37a55eff9e855b449076b65837b91.png?size=128")
    message = await ctx.channel.send(embed=helpEmbed)  # Sends the Embed
    await message.add_reaction("❌")

    def check(reaction, user): # Checks and deletes the menu after no interaction
        return user == ctx.author and str(reaction.emoji) in ["❌"]
        # This makes sure nobody except the command sender can interact with the "menu".

    while True:
        try:  # Makes sure the timer doesn't run out
            reaction, user = await bot.wait_for("reaction_add", timeout=180, check=check)
            # Waiting for a reaction to be added - times out after x seconds, 60 in this
            if str(reaction.emoji) == "❌":
                await message.delete()
        except asyncio.TimeoutError:  # Deletes the message after x seconds
            await message.delete()
            break


@bot.command()  # Ping command
async def ping(ctx):
    ping = bot.latency * 1000  # Multiplies the latency by 1000 to get milliseconds
    pingEmbed = discord.Embed(title="Pong! :ping_pong:", description=f"My latency is: **{int(ping)}ms**", color=0xB87DDF)
    await ctx.channel.send(embed=pingEmbed)  # Sends the embed


@bot.command()  # :)
async def monke(ctx):
    await ctx.channel.send(
        "https://tenor.com/view/obese-monkey-fat-monkey-summer-belly-eating-lettuce-summer-look-gif-13014350"
    )


@bot.command()  # Repeat command
async def repeat(ctx, *, userinput = None):
    sentByMention = str(ctx.author.mention)
    for s in config['bannedWords']:
        # Reads from the bannedWords list and removes anything on the list from the text
        userinput = userinput.replace(s, '')
    # Defining the embed to be used and it's field
    repeatEmbed = discord.Embed(description=userinput, color=0xB87DDF)
    repeatEmbed.add_field(name="Sent by:", value=sentByMention)
    if userinput:  # The If statement that checks for "im" or "@everyone"/"@here"
        if userinput.lower().startswith("im"):
            await ctx.send("yea we know")
        elif userinput.lower().startswith('i '):
            await ctx.send("yea we know")
        elif userinput.lower().startswith("i'm"):
            await ctx.send("yea we know")
        elif userinput.lower() == "@everyone":
            await ctx.send("no :)")
        elif userinput.lower() == "@here":
            await ctx.send("no :)")
        else:  # The else statement that sends the full message if it passes the previous el/if statements
            await ctx.send(embed=repeatEmbed)
    else:  # The else statement that checks if there is no user input argument
        # The error embed that sends if there is no argument
        noUserIn = discord.Embed(title="Error",
                                    description="Sorry! It appears you didn't include something for me to repeat!",
                                    color=0xC73333
                                )  # Makes the embed for if there is no user input
        await ctx.channel.send(embed=noUserIn)


@bot.command()  # 8Ball module (used to be a separate file but caused issues)
async def ask(ctx, *, content):
    import random
    # Defines the array of responses
    responses = ["It is certain", "Without a doubt", "You may rely on it", "Yes, definitely", "It is decidedly so",
            "As I see it, yes", "Most likely", "Yes", "Outlook good", "Signs point to yes", "Reply hazy try again",
            "Better not tell you now", "Ask again later", "Cannot predict now", "Concentrate and ask again",
            "Don't count on it", "Outlook not so good", "My sources say no", "Very doubtful", "My reply is no"]
    answer = random.choice(responses)  # Gets a random response
    await ctx.channel.send(answer)  # Sends the answer


@bot.command() # Fibonacci nth number
async def fibonacci(ctx, num: int):
    fibArray = [0, 1]

    def fibonacci(n):
        if n < 0:
            raise ValueError("Cannot use below 0")
        elif n <= len(fibArray):
            return fibArray[n - 1]
        else:
            temp_fib = fibonacci(n - 1) + fibonacci(n - 2)
            fibArray.append(temp_fib)
            return temp_fib
    try:
        fibNum = fibonacci(num)
        fibonacciEmbed = discord.Embed(title=f"The {num}th Number of the Fibonacci Sequence is:",
                                       description=fibNum,
                                       color=0xB87DDF)
        await ctx.channel.send(embed=fibonacciEmbed)
    except:
        fiboError = discord.Embed(title="Invalid Input",
                                  description="Did you use a negative, invalid, or an input that's too high?",
                                  color=0xC73333
                                  )
        await ctx.channel.send(embed=fiboError)


@bot.command() # Dice roll
async def roll(ctx, sides: int = 6):
    if len(str(sides)) > 256:
        tooBigEmbed = discord.Embed(title="Error: Too Long",
                                    description="You entered a number that filled up the embed's title, please use a shorter one.",
                                    color=0xC73333
                                    )
        await ctx.channel.send(embed=tooBigEmbed)

    elif sides < 0:
        negEmbed = discord.Embed(title="...",
                                    description=f"*Somehow rolls a {sides} sided die*\n\nGood job, you broke the laws of physics. As we speak a black hole has formed and will envelop the universe in less than 24 hours. Hope you're happy jerk.",
                                    color=0xC73333
                                    )
        await ctx.channel.send(embed=negEmbed)

    elif sides == 0:
        zeroEmbed = discord.Embed(title="Yeah, sure",
                                    description="Good luck with that.",
                                    color=0xC73333
                                    )
        await ctx.channel.send(embed=zeroEmbed)
    else:
        roll = randint(1, sides)
        dieEmbed = discord.Embed(title=f"You Rolled a {sides} sided die",
                                 description=f"You rolled a __**{roll}**__!",
                                 color=0xB87DDF)
        await ctx.channel.send(embed=dieEmbed)


@bot.command()  # Calculate Pi to the Nth digit using Chudnovsky's Algorithm
async def pi(ctx, num: int):
    def compute_pi(n):
        decimal.getcontext().prec = n + 1
        C = 426880 * decimal.Decimal(10005).sqrt()
        K = 6.
        M = 1.
        X = 1
        L = 13591409
        S = L
        for i in range(1, n):
            M = M * (K ** 3 - 16 * K) / ((i + 1) ** 3)
            L += 545140134
            X *= -262537412640768000
            S += decimal.Decimal(M * L) / X
        pi = C / S
        return pi
    try:
        piEmbed = discord.Embed(title=f"Pi to the {num}th Digit is:",
                                description=str(compute_pi(num)),
                                color=0xB87DDF
                                )
        piEmbed.set_footer(text="Disclaimer: Value might be off by a slight amount due to rounding")
        await ctx.channel.send(embed=piEmbed)
    except:
        piError = discord.Embed(title="Error: Invalid Input",
                                description="Invalid input, did you use a negative number?",
                                color=0xC73333
                                )
        await ctx.channel.send(embed=piError)


@bot.command()
async def kanye(ctx):
    response = json.loads(requests.get("https://api.kanye.rest").text)
    kanyeEmbed = discord.Embed(title="Your Kanye Quote:",
                               description=response['quote'],
                               color=0xB87DDF)
    kanyeEmbed.set_footer(text="Generated with the kanye.rest API")
    await ctx.channel.send(embed=kanyeEmbed)


@bot.command()
async def dog(ctx):
    response = json.loads(requests.get("https://dog.ceo/api/breeds/image/random").text)
    dogEmbed = discord.Embed(title="I fetched this dog for you 🦴",
                             color=0xB87DDF)
    dogEmbed.set_image(url=f"{response['message']}")
    dogEmbed.set_footer(text="Generated with the Dog CEO API")
    await ctx.channel.send(embed=dogEmbed)


@bot.command()
async def fox(ctx):
    response = json.loads(requests.get("https://randomfox.ca/floof/").text)
    foxEmbed = discord.Embed(title="I found this image of a fox!",
                             color=0xB87DDF)
    foxEmbed.set_image(url=f"{response['image']}")
    foxEmbed.set_footer(text="Generated with the randomfox.ca API")
    await ctx.channel.send(embed=foxEmbed)


@bot.command()
async def cat(ctx):
    response = json.loads(requests.get("https://some-random-api.ml/img/cat").text)
    catEmbed = discord.Embed(title="I found this image of a cat!",
                             color=0xB87DDF)
    catEmbed.set_image(url=f"{response['link']}")
    await ctx.channel.send(embed=catEmbed)


@bot.command()
async def panda(ctx):
    response = json.loads(requests.get("https://some-random-api.ml/img/panda").text)
    pandaEmbed = discord.Embed(title="I found this image of a panda!",
                             color=0xB87DDF)
    pandaEmbed.set_image(url=f"{response['link']}")
    await ctx.channel.send(embed=pandaEmbed)


@bot.command()
async def redpanda(ctx):
    response = json.loads(requests.get("https://some-random-api.ml/img/red_panda").text)
    redpandaEmbed = discord.Embed(title="I found this image of a red panda!",
                             color=0xB87DDF)
    redpandaEmbed.set_image(url=f"{response['link']}")
    await ctx.channel.send(embed=redpandaEmbed)


@bot.command()
async def birb(ctx):
    response = json.loads(requests.get("https://some-random-api.ml/img/birb").text)
    birbEmbed = discord.Embed(title="I found this image of a birb!",
                             color=0xB87DDF)
    birbEmbed.set_image(url=f"{response['link']}")
    await ctx.channel.send(embed=birbEmbed)


@bot.command()
async def koala(ctx):
    response = json.loads(requests.get("https://some-random-api.ml/img/koala").text)
    koalaEmbed = discord.Embed(title="I found this image of a koala!",
                             color=0xB87DDF)
    koalaEmbed.set_image(url=f"{response['link']}")
    await ctx.channel.send(embed=koalaEmbed)

# /\ General Purpose Commands /\

# \/ Raised Permissions Commands \/


# ------Developer Commands------
@bot.command()  # Lists servers the bot is in
async def servers(ctx):  # Developer command
    servers = list(bot.guilds)
    serversEmbedTitle = f"Connected on {str(len(servers))} servers"
    serversEmbedDesc = "- " + '\n- '.join(guild.name for guild in servers)
    serversEmbed = discord.Embed(title=serversEmbedTitle, description=serversEmbedDesc, color=0xB87DDF)
    notDevEmbed = discord.Embed(title="Error",
                                description="Sorry! It appears you don't have permission to use this command.",
                                color=0xC73333)
    if str(ctx.message.author.id) in config['developers']:
        await ctx.send(embed=serversEmbed)

    else:
        await ctx.channel.send(embed=notDevEmbed)


@bot.command()  # Changes the status
async def status(ctx, *, content):  # Developer command that changes the bot's status
    notDevEmbed = discord.Embed(title="Error",
                              description="Sorry! It appears you don't have permission to use this command.",
                              color=0xC73333)
    if str(ctx.message.author.id) in config['developers']:
        await bot.change_presence(
            activity=discord.Game(
                name=content
            )
        )
    else:
        await ctx.channel.send(embed=notDevEmbed)


@bot.group()  # Sets the database command group
async def database(ctx):
    if ctx.invoked_subcommand is None:  # Gives an error if no subcommand is given
        nullEmbed = discord.Embed(title="Error",
                                  description="Please use 'show' or 'add' to interact with the database",
                                  color=0xC73333
                                  )  # Error Embed
        await ctx.channel.send(embed=nullEmbed)


@database.command()  # Shows the database
async def show(ctx):
    notDevEmbed = discord.Embed(title="Error",
                              description="Sorry! It appears you don't have permission to use this command.",
                              color=0xC73333)  # Error Embed
    if str(ctx.message.author.id) in config['developers']:  # Checks if user is a developer
        servers = list(bot.guilds)  # Gets a list of servers
        mndb = mongoclient['the-random-bot']  # Connects to the database
        servercol = mndb['servers']  # Gets the table
        dbquery = servercol.find()  # Gets the column to iterate through
        empty = ""
        entry = 1
        for data in dbquery:  # Loops through the query
            empty += "```md\n# Entry " + str(entry) + ":\n" + str(data) + "```\n"  # Appends to the empty string
            entry += 1
        await ctx.channel.send(empty)  # Sends the result
    else:
        await ctx.channel.send(embed=notDevEmbed)


@database.command()  # Manually adds an entry to the database [ONLY TO BE USED IN TESTING]
async def add(ctx, serverID, serverName):
    mndb = mongoclient['the-random-bot']  # Connects to the database
    notDevEmbed = discord.Embed(title="Error",
                                description="Sorry! It appears you don't have permission to use this command.",
                                color=0xC73333)  # Error embed
    if str(ctx.message.author.id) in config['developers']:  # Checks if someone is in the developers dictionary
        mndb.servers.insert_one(
            { "serverID" : serverID,
                "serverName": serverName
            }
        )  # Adds to the new entry to the database
        await ctx.channel.send("Added to the database.")
    else:
        await ctx.channel.send(embed=notDevEmbed)


@database.command()  # Manually removes an entry from the database [ONLY TO BE USED IN TESTING]
async def remove(ctx, serverID):
    mndb = mongoclient['the-random-bot']  # Connects to the database
    servercol = mndb["servers"]  # The column to be used
    deleteQuery = { "serverID": serverID }  # The query to be deleted
    notDevEmbed = discord.Embed(title="Error",
                                description="Sorry! It appears you don't have permission to use this command.",
                                color=0xC73333)  # Error Embed
    if str(ctx.message.author.id) in config['developers']:  # Checks if someone is in the developer dictionary
        servercol.delete_one(deleteQuery)  # Deletes the entry
        await ctx.channel.send("Removed from the database.")
    else:
        await ctx.channel.send(embed=notDevEmbed)


@bot.command()  # Makes a developer
async def mkdev(ctx, userid=None, *, devName=None):
    for i in ["<",">","@","!"]:  # Makes @Person work too
        userid = userid.replace(i,'')

    # Embed giving an error if the user is not in the developer array in the config.json file
    notDevEmbed = discord.Embed(title="Error",
                              description="Sorry! It appears you don't have permission to use this command.",
                              color=0xC73333)
    if str(ctx.message.author.id) in config['developers']:  # Checking if a user is a developer
        if not userid or not devName:  # Checking if a user gave proper arguments
            await ctx.channel.send("Usage: ;mkdev <userid> <name>")
            return
        if userid not in config['developers']:  # Checking if a user's id is not in the developer section
            config['developers'][userid] = devName
            await ctx.channel.send("Successfully added <@" + userid + "> as a developer")  # Sends a success message
            with open('config.json', 'w+') as configFile:  # Opens the config.json file
                json.dump(config, configFile, indent=4)
                generate_config_reload()
        else:  # Checks if a user is already a developer
            await ctx.channel.send("Error: " + userid + " is already a developer")
    else:  # What sends the notDevEmbed
        await ctx.channel.send(embed=notDevEmbed)


@bot.command()  # Removes a developer
async def rmdev(ctx, userid=None):
    for i in ["<",">","@","!"]: # Makes @Person work too
        userid = userid.replace(i,'')
    notDevEmbed = discord.Embed(title="Error",
                              description="Sorry! It appears you don't have permission to use this command.",
                              color=0xC73333)  # Error Embed
    if str(ctx.message.author.id) in config['developers']:  # Checks if someone is in the developer dictionary
        if not userid:  # Error to send if no ID is defined
            await ctx.channel.send("Usage: ;rmdev <userid>")
            return
        if userid in config['developers']:  # Continues if an ID is defined
            config['developers'].pop(userid)  # Adds ID to the dictionary
            await ctx.channel.send("Successfully removed <@" + userid + "> as a developer")
            with open('config.json', 'w+') as configFile:  # Writes to config.json
                json.dump(config, configFile, indent=4)
                generate_config_reload()
        else:
            await ctx.channel.send("Error: " + userid + " is not a developer")
    else:
        await ctx.channel.send(embed=notDevEmbed)


@bot.command()  # Lists the developers
async def lsdev(ctx):
    notDevEmbed = discord.Embed(title="Error",
                              description="Sorry! It appears you don't have permission to use this command.",
                              color=0xC73333)  # Error Embed
    if str(ctx.message.author.id) in config['developers']:  # Checks if user is in the developer dictionary
        devsEmbed = discord.Embed(title="List of current developers: ")
        for i in config['developers']:  # Iterates through all developers in the dictionary
            devsEmbed.add_field(value=i, name=config['developers'][i], inline=False)
        await ctx.channel.send(embed=devsEmbed)
    else:
        await ctx.channel.send(embed=notDevEmbed)


# The Token initialization and Checking if config.json exists
if __name__ == '__main__':
    if not os.path.exists('config.json'):
        keysGen = str(input("ERROR: DID NOT FIND A CONFIG.JSON FILE\nWould you like to make a config.json file? (Y/N) ")).lower()
        if keysGen == 'y':
            config = {} # Create the empty dictionary for configuration
            print("----Note: We do not receive your API keys, these are stored in a file on your computer.----")
            print("The config.json file created by this should be considered sensitive. DO NOT share it with anyone.")
            config['ytApiKey'] = str(input("Please input your YouTube API Developer Key: "))
            config['lastFmKey'] = str(input("Please input your last.fm API key: "))
            config['lastFmUA'] = str(input("Please input the User Agent that should be used when requesting from the last.fm API: "))
            config['discordToken'] = str(input("Please input your Discord bot token: "))
            config['bannedWords'] = str(input("Please input a list of words you don't want the bot to repeat, seperated by a comma.")).split(',')
            config['developers'] = {} # Create the empty developers dictionary
            print("The next section will allow you to choose who to give access to developer commands. Developers will be able to change the bot's status, see bot statistics, and add other developers. Make sure you trust anyone you add.")
            print("Who will your first developer be? You'll be able to add other ones through the bot later.")
            config['developers'][str(input("User ID of the first dev: "))] = str(input("Name of the first dev: "))
            print("Setup complete, running the bot...")
            with open('config.json', 'w+') as configFile:
                json.dump(config, configFile, indent=4)
            generate_config_reload()
        elif keysGen == 'n':
            print("Exiting... Please remember to make a config.json file in order for the bot to be fully functional.")
            quit()
        print("Creating... Done! Your self-hosted bot is now live!")
        bot.run(config['discordToken'])
    elif os.path.exists('config.json'):
        with open('config.json') as configFile:
            config = json.load(configFile)
        generate_config_reload()
        bot.run(config['discordToken'])
