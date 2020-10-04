import wikipedia
import discord
import tracemalloc
import os
import asyncio
from discord.ext import commands
from random import *
from dotenv import load_dotenv
# test
client = commands.Bot(command_prefix=';', help_command=None)
tracemalloc.start()
numError = "There was an error! Did you make sure you included a minimum/maximum or to give numbers and not words?"


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="randomness unfold | ;"
        )
    )


@client.group()
async def random(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.channel.send('Error: must include what to randomly generate.')


@client.command()
async def help(ctx):
    page1embed = discord.Embed(title="Page 1",
                               description="Placeholder"
                               )
    contents = ["This is page 1!", "This is page 2!", "This is page 3!", "This is page 4!"]
    pages = 4
    cur_page = 1
    message = await ctx.send(f"Page {cur_page}/{pages}:\n{contents[cur_page - 1]}")
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    await message.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page - 1]}")
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page - 1]}")
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "❌":
                await message.delete()

            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after x seconds


@random.command()
async def article(ctx):
    async def ran_art():
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
            return ran_art()


@random.command()
async def number(ctx, low: int, high: int):
    errorEmbed = discord.Embed(title="Error:",
                               description=numError,
                               color=0xB87DDF)
    try:
        ran = randint(low, high)
        numEmbed = discord.Embed(title="Random Number", description=ran, color=0xB87DDF)
        await ctx.channel.send(embed=numEmbed)
    except discord.Forbidden:
        await ctx.channel.send(embed=errorEmbed)


@client.command()
async def status(ctx, *, content):
    import developers
    dev_list = developers.dev_list["Developers"]["User IDs"]
    if ctx.message.author.id in dev_list:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=content))

    else:
        await ctx.channel.send("Sorry! It appears you don't have permission to use this command.")


@client.command()
async def ping(ctx):
    ping = client.latency * 1000
    pingEmbed = discord.Embed(title="Pong! :ping_pong:", description=f"My latency is: {int(ping)}ms", color=0xB87DDF)
    await ctx.send(embed=pingEmbed)


@client.command()
async def monke(ctx):
    await ctx.send(
        "https://tenor.com/view/obese-monkey-fat-monkey-summer-belly-eating-lettuce-summer-look-gif-13014350"
    )


@client.command()
async def repeat(ctx, *, user_in: str):
    if user_in == str.lower("i am stupid") or str.lower("i'm stupid") or str.lower("im stupid"):
        await ctx.send("yea we know")
    elif user_in == str.lower("I am gay") or str.lower("I'm gay") or str.lower("Im gay"):
        await ctx.send("yea we know")
    else:
        await ctx.send(user_in)


# The Token initialization
load_dotenv()
token = os.getenv('discord_token')
client.run(token)
