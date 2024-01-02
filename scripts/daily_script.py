import datetime
from nba_api.stats.endpoints import playergamelogs
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
    yesterday_str = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    season = "2023-24"

    # Fetch player game logs
    player_stats = fetch_player_game_logs(yesterday_str, yesterday_str, season)

    # Group players by game_id and also get the mapping of game_id to matchup names
    matchup_player_stats, game_id_to_matchup = group_players_by_matchup(player_stats)

    # Display the top players for each game, along with the matchup names
    display_top_players(matchup_player_stats, game_id_to_matchup, top_n=5)
