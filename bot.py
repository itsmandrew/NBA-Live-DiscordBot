from discord.ext import commands
from scripts.daily_script import *
from scripts.general_functions import *
from scripts.player_averages_scripts import *
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

@bot.command()
async def playerstats(ctx, *args):
    # Define the current season
    current_season = "2023-24"  # Adjust this based on the actual current NBA season

    # Combine all arguments into a single string (player_name)
    player_name = ' '.join(args)

    # Fetch player averages for the specified player and season
    player_averages = fetch_player_averages(player_name, current_season)

    if not player_averages:
        # No data available
        embed = discord.Embed(
            title=f"No stats available for {player_name} in the {current_season} season.",
            color=0xFF0000  # Red color
        )
    else:
        # Display player averages in an embedded message
        embed = discord.Embed(
            title=f"{player_name}'s Averages - {current_season} Season",
            color=0x00FF00  # Green color
        )

        # Specify the order in which you want to display the stats
        stats_order = ["Points", "Rebounds", "Assists", "Steals", "Blocks", "3s per Game", 
                       "Field Goal Percentage", "Free Throw Percentage", "Turnovers per Game"]

        for stat in stats_order:
            if stat in player_averages:
                embed.add_field(
                    name=stat,
                    value=f"{player_averages[stat]:.2f}",
                    inline=True
                )

    # Print player_averages to the terminal
    print(f"Player Averages for {player_name}:", player_averages)

    # Send the embedded message to the Discord channel
    await ctx.send(embed=embed)



bot.run(BOT_TOKEN)