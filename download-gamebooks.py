import nfldb
import os
import time
import requests

def convert_season_type(season_type):
    season_type = str(season_type)
    if season_type == "Preseason":
        return "Pre"
    elif season_type == "Regular":
        return "Reg"
    elif season_type == "Postseason":
        return "Post"
    else:
        print "Error converting season type"

def download_xml(season_year, week, season_type, gamekey):

    download_folder = "gamebook-xml"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    root_url = "http://www.nflgsis.com/"
    # superbowl handled differently after 2013
    if season_year >= 2014 and week == 5 and season_type == 'Post':
        week = 4
    # pre season games
    if season_type == "Pre":
        week += 1
    # post season games
    if week > 17:
        week = week - 17
    # add leading zero
    if week < 10:
        week = "0" + str(week)
    url = root_url + str(season_year) + "/" + str(season_type) + "/" + str(week)  + "/" + str(gamekey) + "/Gamebook.xml"
    filename = download_folder + "/" + str(season_year) + "-" + str(week) + "-" + season_type + "-" + gamekey + ".xml"
    res = requests.get(url)
    if res.status_code == 200:
        print "Saving %s as %s" % (url, filename)
        with open(filename, "w") as text_file:
            text_file.write(res.content)
    else:
        print "HTTP Response: %d Bad gamebook data for %s" % (res.status_code, url)

    # be nice and sleep 1 seconds between requests
    time.sleep(1)

db = nfldb.connect()
#years = range(1998, 2015)
years = [2015]
for year in years:
    q = nfldb.Query(db)
    #q.game(season_year=year)
    q.game(season_year=year, week=10, season_type='Regular')
    games = sorted(q.as_games(), key=lambda g: g.gsis_id)
    for game in games:
        download_xml(game.season_year, game.week, convert_season_type(game.season_type), game.gamekey)
