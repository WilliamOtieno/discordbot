from discord.ext import commands

import secrets

bot = commands.Bot(command_prefix=".")


@bot.event
async def on_ready():
    print("I am alive.")


@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')


@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


bot.run(secrets.token)
