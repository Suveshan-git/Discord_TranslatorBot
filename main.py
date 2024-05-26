# Install the discord package to import below
import discord
from discord.ext import commands

# Install the python-dotenv package to import
from dotenv import load_dotenv
from typing import Final
import os

# Load the bot token from .env file
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Setup bot to be interactive
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Set the bot command prefix and remove the default help function
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')


@bot.event  # Notification that the bot is ready to use once run
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Run the bot using the bot token
bot.run(TOKEN)
