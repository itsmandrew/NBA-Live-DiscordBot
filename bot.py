"""
Discord Bot for fetching and displaying NBA stats.
"""

import json
import datetime
import discord
from discord.ext import commands
from scripts.daily_script import fetch_player_game_logs, group_players_by_matchup, build_table
from scripts.player_averages_scripts import fetch_player_averages, fetch_player_stats_recent

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
    ''' Displays information about available bot commands in a table format '''
    help_message = "**Available Commands:**\n"

    # Create a Discord Embed
    embed = discord.Embed(
        title="Bot Commands",
        color=discord.Color.blue()
    )

    # Add fields to the Embed for each command in a table-like format
    for command in bot.commands:
        # Exclude the default !help command
        if command.name != 'help':
            embed.add_field(name=f"!{command.name}", value=command.callback.__doc__, inline=False)

    await ctx.send(embed=embed)



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
    '''
    Returns the top 5 fantasy players from each game played today based off ESPN's point system.
    
    Syntax: !daily'''
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
    '''
    Takes in a player name as an argument (e.g., LeBron James) and 
    returns the current season's stats for that specific player.
    
    Syntax: !playerstats <Player Name>'''
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

    await ctx.send(embed=embed)


@bot.command()
async def playerstatsrecent(ctx, *args):
    '''
    Takes in a player name and a number 'n' to fetch recent game stats for that player.
    
    Syntax: !playerstatsrecent <Player Name> <Number of Games>'''
    try:
        # Combine all words except the last one as the player's name
        player_name = ' '.join(args[:-1])
        player_name = ' '.join([word.capitalize() for word in player_name.split()])

        # Extract the last argument as the value of n
        n = int(args[-1])

        # Fetch recent game stats for the player
        player_stats_recent = fetch_player_stats_recent(player_name, n, "2023-24")

        # Create a Discord Embed
        embed = discord.Embed(
            title=f"Recent Game Stats for {player_name}",
            description=f"Last {n} games in the 2023-24 season",
            color=discord.Color.green()
        )

        # Add a field for each individual game
        for game in player_stats_recent:
            game_title = game['Date']
            game_table = f"```PTS: {game['PTS']}, REB: {game['REB']}, AST: {game['AST']}, "
            game_table += f"STL: {game['STL']}, BLK: {game['BLK']}, 3PM: {game['3PM']}, "
            game_table += f"FGM/FGA: {game['FGM']}/{game['FGA']}, "
            game_table += f"FTM/FTA: {game['FTM']}/{game['FTA']}, TO: {game['TO']}```"

            # Add the game table as a field in the Embed
            embed.add_field(
                name=game_title,
                value=game_table,
                inline=False
            )

        await ctx.send(embed=embed)

    except ValueError as e:
        await ctx.send(f"Error: {e}")





bot.run(BOT_TOKEN)
