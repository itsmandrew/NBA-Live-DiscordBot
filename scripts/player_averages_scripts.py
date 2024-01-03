import datetime
from nba_api.stats.endpoints import playergamelogs, commonallplayers
from scripts.general_functions import *
from table2ascii import table2ascii as t2a, PresetStyle


def fetch_player_averages(player_name, season):
    try:
        player_logs = playergamelogs.PlayerGameLogs(
            player_id_nullable=get_player_id_by_name(player_name),
            season_nullable=season
        )
        player_stats = player_logs.get_normalized_dict()['PlayerGameLogs']

        if not player_stats:
            return {}
        
        # Print keys for the first game entry
        sample_game_entry = player_stats[0] if player_stats else {}
        print(f"Keys for one game entry: {sample_game_entry.keys()}")

        # Initialize counters for various stats
        total_games = len(player_stats)
        total_points = sum(game.get("PTS", 0) for game in player_stats)
        total_rebounds = sum(game.get("REB", 0) for game in player_stats)
        total_assists = sum(game.get("AST", 0) for game in player_stats)
        total_steals = sum(game.get("STL", 0) for game in player_stats)
        total_blocks = sum(game.get("BLK", 0) for game in player_stats)
        total_three_pointers = sum(game.get("FG3M", 0) for game in player_stats)
        total_field_goals_made = sum(game.get("FGM", 0) for game in player_stats)
        total_field_goals_attempted = sum(game.get("FGA", 0) for game in player_stats)
        total_free_throws_made = sum(game.get("FTM", 0) for game in player_stats)
        total_free_throws_attempted = sum(game.get("FTA", 0) for game in player_stats)
        total_turnovers = sum(game.get("TOV", 0) for game in player_stats)


        # Calculate averages
        averages = {
            "Points": total_points / total_games,
            "Rebounds": total_rebounds / total_games,
            "Assists": total_assists / total_games,
            "Steals": total_steals / total_games,
            "Blocks": total_blocks / total_games,
            "3s per Game": total_three_pointers / total_games,
            "Field Goal Percentage": (total_field_goals_made / total_field_goals_attempted) * 100,
            "Free Throw Percentage": (total_free_throws_made / total_free_throws_attempted) * 100,
            "Turnovers per Game": total_turnovers / total_games,
        }

        return averages

    except Exception as e:
        print(f"Error fetching player averages for {player_name}: {e}")
        return {}