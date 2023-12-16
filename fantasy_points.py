from nba_api.stats.endpoints import playergamelogs
import datetime



yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
yesterday_str = yesterday.strftime("%m/%d/%Y")

# Fetch player game logs for the specified date range
try:
    player_logs = playergamelogs.PlayerGameLogs(
        date_from_nullable="12/15/2023",
        date_to_nullable="12/16/2023",
        season_nullable="2023-24"
    )
    player_stats = player_logs.get_normalized_dict()['PlayerGameLogs']
except Exception as e:
    print(f"Error fetching data: {e}")
    player_stats = []


# Calculate fantasy points for each player's performance on the specified date
fantasy_scores = []
for entry in player_stats:
    print(entry)
