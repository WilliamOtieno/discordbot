import discord
import secrets
from discord.ext import commands


client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print("I am alive.")

client.run(secrets.token)