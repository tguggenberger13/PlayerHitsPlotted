import matplotlib.pyplot as plt
import requests
from matplotlib import image
from hockey_rink import NHLRink
from PIL import Image
from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import seaborn as sns

player_to_chart = "Matt Dumba"
team_of_player = "MIN"
#https://statsapi.web.nhl.com/api/v1/teams
team_id = "30"

#All MIN games
fig=plt.figure(figsize=(10,10))
plt.xlim([0,100])
plt.ylim([-42.5, 42.5])
xc=[]
yc=[]
#seasons = ["20192020","20202021","20212022"]
seasons = ["20212022"]
shot_attempts = 0
sog = 0
goals = 0
hits = 0
for season in seasons:
    min_schedule = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?season="+season+"&teamId="+team_id+"&gameType=R")
    schedule = min_schedule.json()
    schedule = schedule["dates"]

    game_ids=[]
    for game in schedule:
        game_data=game["games"]
        game_data=(game_data[0])
        status = game_data["status"]
        status = status["abstractGameState"]
        if status == "Preview":
            continue
        else:
            id = game_data["gamePk"]
            game_ids.append(id)

    for ids in game_ids:
        url = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + str(ids) + "/feed/live")
        content = url.json()

        event = content["liveData"]
        game_data = content["gameData"]
        date = game_data["datetime"]
        datetime = date["dateTime"]
        datetime = datetime[0:10]
        teams = game_data["teams"]
        away = teams["away"]
        home = teams["home"]
        away_team = away["abbreviation"]
        home_team = home["abbreviation"]
        plays = event["plays"]
        all_plays = plays["allPlays"]
        if home_team == team_of_player:
            team_to_chart = home_team
        else:
            team_to_chart = away_team
        for i in all_plays:
            result = i["result"]
            event = result["event"]
            if event=="Hit":
                team_info = i["team"]
                team = team_info["triCode"]
                if team == team_to_chart:
                    players = (i["players"])
                    player = (players[0])
                    player = (player["player"])
                    player = (player["fullName"])
                    if player == player_to_chart:
                        shot_attempts += 1
                        print(player)
                        print(team)
                        print(event)
                        coords = (i["coordinates"])
                        print(coords)
                        print()
                        x = int(coords["x"])
                        y = int(coords["y"])
                        #plt.plot(x, y, 'd', color="#4bad53",markersize=20)
#                         if x < 0:
#                             x = abs(x)
#                             xc.append(x)
#                             y = y*-1
#                             yc.append(y)
#                             #plt.plot(x, y, 'o', color="#f0a911",markersize=15)

#                         else:
#                             x=x
#                             xc.append(x)
#                             y=y
#                             yc.append(y)
#                            # plt.plot(x, y, 'o', color="#f0a911",markersize=15)
                   
                        if event=="Hit":
                            hits+=1
                            plt.plot(x, y, 'X', color="#4bad53",markersize=10)
                    
#                         elif event=="Shot":
#                             sog+=1
#                             plt.plot(x, y, '.', color="#f0a911",markersize=15)
                        
            else:
                continue


rink = NHLRink()
ax = rink.draw()
# hb = ax.hexbin(xc, yc, gridsize=25, cmap='Reds')
# ax.clear()
# ax = rink.draw(display_range="ozone")
# cb = fig.colorbar(hb, ax=ax, label='Shot Frequency')
# kde = sns.kdeplot(xc,yc, shade = True, shade_lowest = False, alpha=1, cmap="Reds")


plt.title( player_to_chart + ": All Hits: 2021-2022\n" + str(shot_attempts) + " Hits")
plt.show()
