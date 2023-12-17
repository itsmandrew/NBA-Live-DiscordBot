from discord.ext import commands
from daily_script import display_top_players, group_players_by_matchup, fetch_player_game_logs, build_table_for_matchup
import discord
import json
import datetime
from table2ascii import table2ascii as t2a, PresetStyle

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
    channel = bot.get_channel(CHANNEL_ID)

    await channel.send("Salmaan sucks at fantasy")

@bot.command() 
async def stats(ctx):
    
    await ctx.send("Checking stats")


@bot.command()
async def daily(ctx):
    yesterday_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    season = "2023-24"

    player_stats = fetch_player_game_logs(yesterday_str, yesterday_str, season)
    matchup_player_stats, game_id_to_matchup = group_players_by_matchup(player_stats)

    # Creating a Discord Embed
    embed = discord.Embed(title="NBA Fantasy Points Summary", color=discord.Color.blue())

    for game_id, players in matchup_player_stats.items():
        formatted_matchup = game_id_to_matchup[game_id]  # Fetch the matchup string
        table_str = build_table_for_matchup(formatted_matchup, players)
        embed.add_field(name=f"**{formatted_matchup} ({game_id})**", value=table_str, inline=False)

    if not embed.fields:
        embed.description = "No data available for the specified date."

    await ctx.send(embed=embed)

bot.run(BOT_TOKEN)