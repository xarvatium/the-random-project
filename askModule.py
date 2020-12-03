import discord
import random
from discord.ext import commands
client = commands.Bot(command_prefix=';', help_command=None)

@client.command()
async def ask(ctx, *, content):
    responses = ["It is certain", "Without a doubt", "You may rely on it", "Yes, definitely", "It is decidedly so",
            "As I see it, yes", "Most likely", "Yes", "Outlook good", "Signs point to yes", "Reply hazy try again",
            "Better not tell you now", "Ask again later", "Cannot predict now", "Concentrate and ask again",
            "Don't count on it", "Outlook not so good", "My sources say no", "Very doubtful", "My reply is no"]
    answer = random.choice(responses)
    await ctx.channel.send(answer)