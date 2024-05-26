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


@bot.group(invoke_without_command=True)  # Custom help function to describe how to use the bot and what other commands the bot has
async def help(ctx):
    embed = discord.Embed(
        title="Help",
        description="TranslatorBot allows you to translate any message into another language! You can learn more about how to use the bot with the functions below:\n",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="How to translate a message?",
        value="```\n!translate <target_language_code> <message>\n```",
        inline=False
    )
    embed.add_field(
        name="Translate example",
        value="```\n!translate fr Hello, how are you?\n```",
        inline=False
    )
    embed.add_field(
        name="How to get a list of Language codes?",
        value="The command below will bring up a list of language codes you can use to translate your message into:```\n!language_codes\n```",
        inline=False
    )
    await ctx.send(embed=embed)

# Run the bot using the bot token
bot.run(TOKEN)
