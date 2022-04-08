# bot.py
import os

import discord
from dotenv import load_dotenv

# Load token from environment file
load_dotenv()
TOKEN = os.getenv("token")
# Initialize discord bot
bot = discord.Client()
# This runs when the bot has connected to discord
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to discord...")
    print(f"Bot servers: ")
    for server in bot.guilds:
        print(f"Server name: {server.name}, Server ID: {server.id}")
    # Send a message to a text channel
    # await bot.get_channel(<your_channel_id_here>).send("bot is online")


bot.run(TOKEN)

