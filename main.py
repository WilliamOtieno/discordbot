from discord.ext import commands, tasks
from itertools import cycle
import secrets
import random
import discord
import os

bot = commands.Bot(command_prefix="/")
status = cycle(['GTA V', 'Chess'])


@bot.event
async def on_ready():
    change_status.start()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Something nice"))
    print("Samaritan online")


@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')


@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


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


@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    print(f"Cleared {amount} messages")


@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")


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


@bot.command()
async def load(extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command()
async def unload(extension):
    bot.unload_extension(f"cogs.{extension}")


@bot.command()
async def reload(extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

if __name__ == '__main__':
    bot.run(secrets.token)
