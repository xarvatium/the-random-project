# ---------------------------------------
# Made by Xarvatium#6561 with support from David J Horine#6457 and mdp189#8180
# --My Socials--
# Github: https://github.com/xarvatium
# ---------------------------------------

import asyncio
from generate import *
from pymongo import MongoClient
mongoclient = MongoClient('mongodb://localhost:27017')




# Having helpText assigned here will cause helptext to only get read once, reducing disk access
helpText = {}
with open('helpText') as helpFile:
    helpString = helpFile.read()
helpText['general'] = helpString.split("<general>\n")[1].split("\n</general>")[0]
helpText['random'] = helpString.split("<random>\n")[1].split("\n</random>")[0]


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


# ------General Commands------
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
    helpEmbed.add_field(name="Random Generator Commands",
                        value=helpText['random'],
                        inline=False
                        )  # Defines the random portion of the section
    helpEmbed.set_footer(text="Creator: Xarvatium#6561", icon_url="https://cdn.discordapp.com/avatars/514866599400833034/88a61a2683879b72622d4f9990dc6d2b.png?size=128")
    helpEmbed.set_author(name="The Random Bot", icon_url="https://cdn.discordapp.com/avatars/755986454907191319/39f37a55eff9e855b449076b65837b91.png?size=128")
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
    await ctx.send(embed=pingEmbed)  # Sends the embed


@bot.command()  # :)
async def monke(ctx):
    await ctx.send(
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


@bot.command()  # Support Command
async def support(ctx):
    supportEmbed = discord.Embed(title="Support",
                                 description="Hi, if you need support, please join the [Development Server](https://discord.gg/3hry5EFuM4) or head over to the GitHub page and open an [issue](https://github.com/xarvatium/the-random-project/issues).")
    await ctx.channel.send(embed=supportEmbed)

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
