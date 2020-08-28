from discord.ext import commands, tasks
from itertools import cycle
import secrets
import random
import discord
import os
import json


def get_prefix(bot, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=get_prefix)
status = cycle(['GTA V', 'Chess', 'Checkers', 'Minecraft'])


# Bot coming online
@bot.event
async def on_ready():
    change_status.start()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Something nice"))
    print("Samaritan online")


# When someone joins
@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')


# When member leaves
@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


# When wrong command is used
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")


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
    print(f"Cleared {amount} messages")


# Kick user
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")


# Ban user
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")


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


def is_it_me(ctx):
    return ctx.author.id == 693701426953584691


@bot.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f"Hi I'm {ctx.author}.")


@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
        f.close()

    prefixes[str(guild.id)] = "/"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
        f.close()


@bot.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
        f.close()

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
        f.close()


@bot.command()
async def change_prefix(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
        f.close()

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
        f.close()


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

if __name__ == '__main__':
    bot.run(secrets.token)
