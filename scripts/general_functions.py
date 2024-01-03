import datetime
from nba_api.stats.endpoints import playergamelogs, commonallplayers
from table2ascii import table2ascii as t2a, PresetStyle

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