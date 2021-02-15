import discord
import random
from discord.ext import commands
bot = commands.Bot(command_prefix=';', help_command=None)

# Defines the Ask command
@bot.command()
async def ask(ctx, *, content):
    # Defines the Response array that the randomizer chooses from
    responses = ["It is certain", "Without a doubt", "You may rely on it", "Yes, definitely", "It is decidedly so",
            "As I see it, yes", "Most likely", "Yes", "Outlook good", "Signs point to yes", "Reply hazy try again",
            "Better not tell you now", "Ask again later", "Cannot predict now", "Concentrate and ask again",
            "Don't count on it", "Outlook not so good", "My sources say no", "Very doubtful", "My reply is no"]
    answer = random.choice(responses)
    # The interaction with Discord
    await ctx.channel.send(answer)