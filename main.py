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


@bot.command()  # Gives a list of language codes the bot can use in a pagination format for ease of use and saving space
async def language_codes(ctx):
    language_codes = {
        "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
        "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be", "Bengali": "bn", "Bosnian": "bs",
        "Bulgarian": "bg", "Catalan": "ca", "Cebuano": "ceb", "Chinese (Simplified)": "zh-CN",
        "Chinese (Traditional)": "zh-TW", "Corsican": "co", "Croatian": "hr", "Czech": "cs",
        "Danish": "da", "Dutch": "nl", "English": "en", "Esperanto": "eo", "Estonian": "et",
        "Filipino": "tl", "Finnish": "fi", "French": "fr", "Frisian": "fy", "Galician": "gl",
        "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu", "Haitian Creole": "ht",
        "Hausa": "ha", "Hawaiian": "haw", "Hebrew": "iw", "Hindi": "hi", "Hmong": "hmn",
        "Hungarian": "hu", "Icelandic": "is", "Igbo": "ig", "Indonesian": "id", "Irish": "ga",
        "Italian": "it", "Japanese": "ja", "Javanese": "jv", "Kannada": "kn", "Kazakh": "kk",
        "Khmer": "km", "Korean": "ko", "Kurdish": "ku", "Kyrgyz": "ky", "Lao": "lo", "Latin": "la",
        "Latvian": "lv", "Lithuanian": "lt", "Luxembourgish": "lb", "Macedonian": "mk",
        "Malagasy": "mg", "Malay": "ms", "Malayalam": "ml", "Maltese": "mt", "Maori": "mi",
        "Marathi": "mr", "Mongolian": "mn", "Myanmar (Burmese)": "my", "Nepali": "ne",
        "Norwegian": "no", "Nyanja (Chichewa)": "ny", "Odia (Oriya)": "or", "Pashto": "ps",
        "Persian": "fa", "Polish": "pl", "Portuguese (Portugal, Brazil)": "pt", "Punjabi": "pa",
        "Romanian": "ro", "Russian": "ru", "Samoan": "sm", "Scots Gaelic": "gd", "Serbian": "sr",
        "Sesotho": "st", "Shona": "sn", "Sindhi": "sd", "Sinhala (Sinhalese)": "si",
        "Slovak": "sk", "Slovenian": "sl", "Somali": "so", "Spanish": "es", "Sundanese": "su",
        "Swahili": "sw", "Swedish": "sv", "Tagalog (Filipino)": "tl", "Tajik": "tg", "Tamil": "ta",
        "Tatar": "tt", "Telugu": "te", "Thai": "th", "Turkish": "tr", "Turkmen": "tk",
        "Ukrainian": "uk", "Urdu": "ur", "Uyghur": "ug", "Uzbek": "uz", "Vietnamese": "vi",
        "Welsh": "cy", "Xhosa": "xh", "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu",
    }

    # Create a list of embeds for pagination
    embeds = []
    chunk_size = 25  # Number of language codes per embed
    items = list(language_codes.items())

    for i in range(0, len(items), chunk_size):
        embed = discord.Embed(
            title="Language Codes",
            description="Here are the available language codes for translation.",
            color=discord.Color.blue()
        )
        chunk = items[i:i + chunk_size]
        for language, code in chunk:
            embed.add_field(name=language, value=code, inline=True)
        embed.set_footer(text=f"Page {len(embeds) + 1}")
        embeds.append(embed)

    # Send the first embed
    current_page = 0
    message = await ctx.send(embed=embeds[current_page])

    # Add reaction buttons
    if len(embeds) > 1:
        await message.add_reaction("⬅️")  # Previous page
        await message.add_reaction("➡️")  # Next page

    # Define check function for reaction events
    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in ["⬅️", "➡️"]

    # Pagination loop
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)

            # Handle reaction events
            if str(reaction.emoji) == "➡️" and current_page < len(embeds) - 1:
                current_page += 1
                await message.edit(embed=embeds[current_page])
                await message.remove_reaction("➡️", user)
            elif str(reaction.emoji) == "⬅️" and current_page > 0:
                current_page -= 1
                await message.edit(embed=embeds[current_page])
                await message.remove_reaction("⬅️", user)

        except TimeoutError:
            break


# Run the bot using the bot token
bot.run(TOKEN)
