"""
Discord Bot for fetching and displaying NBA stats.
"""

import json
import datetime
import discord
from discord.ext import commands
from scripts.daily_script import fetch_player_game_logs, group_players_by_matchup, build_table
from scripts.player_averages_scripts import fetch_player_averages

FILE_PATH = 'creds.json'  # Replace with your actual file path

with open(FILE_PATH, 'r', encoding='utf-8') as json_file:
    loaded_data = json.load(json_file)

# Extracting data into variables
BOT_TOKEN = loaded_data.get("BOT_TOKEN", "")
CHANNEL_ID = loaded_data.get("CHANNEL_ID", "")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    ''' Initializes the Discord Bot, will print message when ran '''
    print("Bot is ready.")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Salmaan sucks at fantasy")

@bot.command()
async def helpme(ctx):
    ''' Displays information about available bot commands '''
    help_message = "**Available Commands:**\n\n"

    for command in bot.commands:
        # Exclude the default !help command
        if command.name != 'help':
            help_message += f"**!{command.name}:** {command.callback.__doc__}\n"

    await ctx.send(help_message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send(f"Error: {error}")


@bot.command()
async def stats(ctx):
    ''' Test function '''
    await ctx.send("Checking stats")

@bot.command()
async def daily(ctx):
    ''' Returns the top 5 fantasy players from each game 
    played today based off ESPN's point system'''
    yesterday_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    season = "2023-24"

    player_stats = fetch_player_game_logs(yesterday_str, yesterday_str, season)
    matchup_player_stats, game_id_to_matchup = group_players_by_matchup(player_stats)

    embed = discord.Embed(title="NBA Fantasy Points Summary", color=discord.Color.blue())

    for game_id, players in matchup_player_stats.items():
        formatted_matchup = game_id_to_matchup[game_id]  # Fetch the matchup string
        table_str = build_table(formatted_matchup, players)
        embed.add_field(name=f"**{formatted_matchup} ({game_id})**", value=table_str, inline=False)

    if not embed.fields:
        embed.description = "No data available for the specified date."

    await ctx.send(embed=embed)

@bot.command()
async def playerstats(ctx, *args):
    ''' Takes in a player name as an argument eg. Lebron James, and 
    returns the current seasons stats for that specific player '''
    current_season = "2023-24"  # Adjust this based on the actual current NBA season
    player_name = ' '.join([word.capitalize() for word in args])  # Combine to one string

    player_averages = fetch_player_averages(player_name, current_season)

    if not player_averages:
        embed = discord.Embed(
            title=f"No stats available for {player_name} in the {current_season} season.",
            color=0xFF0000  # Red color
        )
    else:
        embed = discord.Embed(
            title=f"{player_name}'s Averages - {current_season} Season",
            color=0x00FF00  # Green color
        )

        stats_order = ["Points", "Rebounds", "Assists", "Steals", "Blocks", "3s per Game",
                       "Field Goal Percentage", "Free Throw Percentage", "Turnovers per Game"]

        for stat in stats_order:
            if stat in player_averages:
                embed.add_field(
                    name=stat,
                    value=f"{player_averages[stat]:.2f}",
                    inline=True
                )

    # print(f"Player Averages for {player_name}:", player_averages)
    await ctx.send(embed=embed)

bot.run(BOT_TOKEN)
