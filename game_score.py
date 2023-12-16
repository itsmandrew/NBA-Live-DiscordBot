from nba_api.stats.static import teams
from nba_api.stats.endpoints import scoreboard
import datetime

# Function to create a mapping of team IDs to team names
def get_team_id_name_map():
    all_teams = teams.get_teams()
    return {team['id']: team['full_name'] for team in all_teams}

# Get the team ID to name mapping
team_id_name_map = get_team_id_name_map()

# Get yesterday's date
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")

# Fetch the scoreboard for yesterday's games
try:
    scoreboard_data = scoreboard.Scoreboard(game_date=yesterday_str)
    line_score = scoreboard_data.line_score.get_data_frame()
except Exception as e:
    print(f"Error fetching data: {e}")
    line_score = None

# Check if line score data is available
if line_score is None or line_score.empty:
    print("No score data available for games on this date.")
else:
    # Grouping by GAME_ID
    grouped_scores = line_score.groupby('GAME_ID')

    # Iterating through each game
    for game_id, game_data in grouped_scores:
        teams_scores = []
        for index, row in game_data.iterrows():
            team_id = row['TEAM_ID']
            team_points = row['PTS']
            team_name = team_id_name_map.get(team_id, 'Unknown')
            teams_scores.append((team_name, team_points))

        # Assuming two teams per game, format the output
        if len(teams_scores) == 2:
            print(f"{teams_scores[0][0]} vs {teams_scores[1][0]}: {teams_scores[0][1]} - {teams_scores[1][1]}")
        else:
            print(f"Game {game_id} data is incomplete.")
