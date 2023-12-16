from nba_api.stats.endpoints import playergamelogs
import datetime

# Fetch player game logs for the specified date range
try:
    player_logs = playergamelogs.PlayerGameLogs(
        date_from_nullable="12/15/2023",
        date_to_nullable="12/15/2023",
        season_nullable="2023-24"
    )
    player_stats = player_logs.get_normalized_dict()['PlayerGameLogs']
except Exception as e:
    print(f"Error fetching data: {e}")
    player_stats = []

# Group players by matchup
matchup_player_stats = {}
for entry in player_stats:
    matchup = entry['MATCHUP']
    player_name = entry['PLAYER_NAME']
    fantasy_points = entry['NBA_FANTASY_PTS']

    if matchup not in matchup_player_stats:
        matchup_player_stats[matchup] = []
    matchup_player_stats[matchup].append((player_name, fantasy_points))

# Sort and get top 5 players for each matchup
for matchup, players in matchup_player_stats.items():
    # Replace '@' with 'vs'
    formatted_matchup = matchup.replace(' @ ', ' vs ')
    top_players = sorted(players, key=lambda x: x[1], reverse=True)[:5]
    print(f"Matchup {formatted_matchup} -------------------------- :")
    for player, score in top_players:
        print(f"   -{player}: {score} fantasy points")
    print()
