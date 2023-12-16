from nba_api.live.nba.endpoints import scoreboard

# Today's Score Board
games = scoreboard.ScoreBoard()

# json
games = games.get_dict()

#print(games["scoreboard"]["games"])

# Save for later... gets me ALL games played today
# for g in games["scoreboard"]["games"]:
#     #print(g.keys())
#     home_team = g["homeTeam"]["teamCity"] + " " + g["homeTeam"]["teamName"]
#     away_team = g["awayTeam"]["teamCity"] + " " + g["awayTeam"]["teamName"]
#     print(home_team + " plays " + away_team)


for g in games["scoreboard"]["games"]:
    print(g['gameLeaders'])