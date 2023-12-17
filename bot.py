from discord.ext import commands
import discord
import json


# Define the path to your JSON file
file_path = 'creds.json'  # Replace with your actual file path

# Reading data from the JSON file
with open(file_path, 'r') as json_file:
    loaded_data = json.load(json_file)

# Extracting data into variables
BOT_TOKEN = loaded_data.get("BOT_TOKEN", "")
CHANNEL_ID = loaded_data.get("CHANNEL_ID", "")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Testing")

bot.run(BOT_TOKEN)