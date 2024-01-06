from nba_api.stats.endpoints import playergamelogs, commonallplayers
from nba_api.stats.library.parameters import LastNGamesNullable
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
    

def fetch_player_stats_recent(player_name, n, season):
    try:
        player_id = get_player_id_by_name(player_name)
        if player_id is None:
            raise ValueError(f"Player {player_name} not found.")

        # Fetch recent game logs for the player
        player_logs = playergamelogs.PlayerGameLogs(
            player_id_nullable=player_id,
            season_nullable=season,
            last_n_games_nullable=LastNGamesNullable()
        )
        player_stats = player_logs.get_normalized_dict()['PlayerGameLogs']

        if not player_stats:
            raise ValueError(f"No game logs found for {player_name} in the {season} season.")

        game_stats_list = []
        # Select the last N games from the list
        for game in player_stats[0:n]:
            raw_date = game.get("GAME_DATE", "")
            formatted_date = raw_date[:10]  # Extract the first 10 characters (YYYY-MM-DD)
            game_stats = {
                "Date": formatted_date,
                "PTS": game.get("PTS", 0),
                "REB": game.get("REB", 0),
                "AST": game.get("AST", 0),
                "STL": game.get("STL", 0),
                "BLK": game.get("BLK", 0),
                "3PM": game.get("FG3M", 0),
                "FGM": game.get("FGM", 0),
                "FGA": game.get("FGA", 0),
                "FTM": game.get("FTM", 0),
                "FTA": game.get("FTA", 0),
                "TO": game.get("TOV", 0),
            }

            game_stats_list.append(game_stats)

        return game_stats_list

    except Exception as e:
        print(f"Error fetching player stats for {player_name}: {e}")
        return []