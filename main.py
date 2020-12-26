from discord.ext import commands, tasks
from itertools import cycle
import secrets
import random
import discord
import os
import time
import requests
import json

bot = commands.Bot(command_prefix=".")
status = cycle(['GTA V', 'Chess', 'Checkers', 'Minecraft', 'Call of Duty'])
sad_words = ["sad", "depressed", "unhappy", "angry", "grave", "hard", "lonely", "sorry", "upset", "troubled", "demise",
             "disappointed", "death", "obituary", "disaster", "funeral", "gloomy", "sombre", "dismal", "rejected",
             "gloomy", "unhappy", "miserable", "angry", "suicide", "suicidal", "kill"]
starter_encouragements = [
    "Cheer up! ",
    "Hang in there. ",
    "You're a great person. ",
    "Don't worry. ",
    "You're only human."
]


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    return quote


# Bot successfully connecting to Discord
@bot.event
async def on_connect():
    print("Samaritan online.")


# Bot disconnecting from Discord
@bot.event
async def on_disconnect():
    print("Samaritan offline.")


# Bot becoming ready to perform its functions
@bot.event
async def on_ready():
    change_status.start()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Something nice"))
    print("I am alive.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content
    if any(word in msg for word in sad_words):
        quote = get_quote()
        await message.channel.send(random.choice(starter_encouragements))
        time.sleep(2)
        await message.channel.send(quote)


# If any errors are experienced
@bot.event
async def on_error():
    print("I am experiencing issues, please check me out.")


# When someone joins
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    print(f'{member} has joined the server.')
    await channel.send(f"Welcome, {member}.")


# When member leaves
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    print(f'{member} has left the server.')
    await channel.send(f"{member} has left us.")


# When wrong command is used
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")
        print("Invalid command used")


# Random answer to question
@bot.command(aliases=["8ball", "ask"])
async def _8ball(ctx, *, question):
    responses = [
        "It is certain",
        "I'm not sure",
        "Dont count on it",
        "My reply is no",
        "My sources say no"
    ]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


# Clear messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    time.sleep(2)
    await ctx.send(f"Cleared {amount} messages.")
    print(f"Cleared {amount} messages")


""" # Dictionary function
@bot.command()
async def dictionary(ctx):
    word = ctx.message.text
    print(word)
    content = requests.get(f"https://api.dictionaryapi.dev/api/v1/entries/en/{word}").json()
    print(content)
    try:
        noun_def = content[0]["meaning"]["noun"][0]["definition"]
        print(noun_def)
        await ctx.send(str(noun_def))
        print("dict")
        time.sleep(0.5)
    except KeyError:
        print("oops")
        pass
"""


# Kick user
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")
    print(f"Kicked {member}")


# Ban user
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")
    print(f"Banned {member}")


# Unban user
@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


# Load cogs
@bot.command()
async def load(extension):
    bot.load_extension(f"cogs.{extension}")


# Unload cogs
@bot.command()
async def unload(extension):
    bot.unload_extension(f"cogs.{extension}")


# Reload cogs
@bot.command()
async def reload(extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")


# Loop a task
@tasks.loop(minutes=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


# Handle exception
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify amount of messages to delete.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You are not my master.")


"""
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I only answer to my master")
"""


def is_it_me(ctx):
    return ctx.author.id == 693701426953584691


@bot.command()
@commands.check(is_it_me)
async def greetings(ctx):
    await ctx.send(f"Hi I'm Samaritan.")


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

if __name__ == '__main__':
    bot.run(secrets.token)
