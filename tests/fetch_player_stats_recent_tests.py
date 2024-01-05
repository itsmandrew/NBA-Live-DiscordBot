import sys
import os

# Get the absolute path to the project directory
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)

from scripts.player_averages_scripts import *
from scripts.general_functions import *
from fetch_player_stats_recent_tests import *
import datetime
from nba_api.stats.endpoints import playergamelogs, commonallplayers
from table2ascii import table2ascii as t2a, PresetStyle



def main():
    player_name = 'LeBron James'
    n = 20
    season = '2023-24'

    result = fetch_player_stats_recent(player_name, n, season)

    print(f"Player Stats for {player_name} in the {n} most recent games:")
    for game_stats in result:
        print(game_stats)

if __name__ == "__main__":
    main()