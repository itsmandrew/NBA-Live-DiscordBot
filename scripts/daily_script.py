import datetime
from nba_api.stats.endpoints import playergamelogs, commonallplayers
from table2ascii import table2ascii as t2a, PresetStyle


def fetch_player_game_logs(date_from, date_to, season):
    try:
        player_logs = playergamelogs.PlayerGameLogs(
            date_from_nullable=date_from,
            date_to_nullable=date_to,
            season_nullable=season
        )
        return player_logs.get_normalized_dict()['PlayerGameLogs']
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    
def get_player_id_by_name(full_name):
    # Fetch all players
    players_data = commonallplayers.CommonAllPlayers().get_normalized_dict()

    # Access the list of players
    players_list = players_data['CommonAllPlayers']

    # Iterate through the list to find the player ID
    for player in players_list:
        if player['DISPLAY_FIRST_LAST'].lower() == full_name.lower():
            return player['PERSON_ID']

    # Return None if no match is found
    return None

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




def group_players_by_matchup(player_stats):

    game_id_to_matchup = {}  # Stores the matchup name for each game ID
    matchup_player_stats = {}  # Stores player stats grouped by game ID

    for entry in player_stats:
        game_id = entry['GAME_ID']
        matchup = entry['MATCHUP'].replace(' @ ', ' vs ')
        player_name = entry['PLAYER_NAME']
        fantasy_points = entry['NBA_FANTASY_PTS']

        # Store the matchup name for each game ID
        game_id_to_matchup[game_id] = matchup

        # Group player stats by game ID
        if game_id not in matchup_player_stats:
            matchup_player_stats[game_id] = []
        matchup_player_stats[game_id].append((player_name, fantasy_points))

    return matchup_player_stats, game_id_to_matchup


def display_top_players(matchup_player_stats, game_id_to_matchup, top_n=5):
    for game_id, players in matchup_player_stats.items():
        formatted_matchup = game_id_to_matchup[game_id]
        top_players = sorted(players, key=lambda x: x[1], reverse=True)[:top_n]

        print(f"Matchup {formatted_matchup} ({game_id}) -------------------------- :")
        for player, score in top_players:
            print(f"   -{player}: {score} fantasy points")
        print()



def build_table_for_matchup(matchup, players, top_n=5):
    top_players = sorted(players, key=lambda x: x[1], reverse=True)[:top_n]
    table_content = [(player, f"{score:.1f}") for player, score in top_players]
    table = t2a(
        header=["Player", "Fantasy Points"],
        body=table_content,
        style=PresetStyle.thin_compact
    )
    return f"```{table}```"




# Main execution
if __name__ == "__main__":
    # yesterday_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    # season = "2023-24"

    # # Fetch player game logs
    # player_stats = fetch_player_game_logs(yesterday_str, yesterday_str, season)

    # # Group players by game_id and also get the mapping of game_id to matchup names
    # matchup_player_stats, game_id_to_matchup = group_players_by_matchup(player_stats)

    # # Display the top players for each game, along with the matchup names
    # display_top_players(matchup_player_stats, game_id_to_matchup, top_n=5)
    # Provide sample data for testing
    sample_player_name = "LeBron James"
    sample_season = "2023-24"

    # Call the function and print the result
    player_averages = fetch_player_averages(sample_player_name, sample_season)
    print(f"Averages for {sample_player_name} in {sample_season} season:")
    print(player_averages)
