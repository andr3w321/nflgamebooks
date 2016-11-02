def get_division(team):
    divisions = [
        {'name': 'afc_east', 'teams': ['NE', 'BUF', 'NYJ', 'MIA']},
        {'name': 'afc_north', 'teams': ['CIN', 'PIT', 'BAL', 'CLE']},
        {'name': 'afc_south', 'teams': ['IND', 'HOU', 'JAC', 'TEN']},
        {'name': 'afc_west', 'teams': ['DEN', 'KC', 'OAK', 'SD']},
        {'name': 'nfc_east', 'teams': ['NYG', 'WAS', 'PHI', 'DAL']},
        {'name': 'nfc_north', 'teams': ['MIN', 'GB', 'CHI', 'DET']},
        {'name': 'nfc_south', 'teams': ['CAR', 'NO', 'ATL', 'TB']},
        {'name': 'nfc_west', 'teams': ['ARI', 'STL', 'SEA', 'SF']}
    ]
    for division in divisions:
        if team in division['teams']:
            return division['name']
            break
    print "Unknown division for {}".format(team)
    return 'UNK'

def get_timezone(team):
    timezones = [
        {'name': 'EST', 'teams': ['ATL', 'BAL', 'BUF', 'CAR', 'CIN', 'CLE', 'DET', 'IND', 'JAC', 'MIA', 'NE', 'NYG', 'NYJ', 'PHI', 'PIT', 'TB', 'WAS']},
        {'name': 'CST', 'teams': ['CHI', 'DAL', 'GB', 'HOU', 'KC', 'MIN', 'NO', 'STL', 'TEN']},
        {'name': 'MT', 'teams': ['ARI', 'DEN']},
        {'name': 'PST', 'teams': ['OAK', 'SD', 'SF', 'SEA']}
    ]
    for timezone in timezones:
        if team in timezone['teams']:
            return timezone['name']
            break
    print "Unknwon timezone for {}".format(team)

#select distinct gamebook.home_team,gamebook.stadium from gamebook where season_year = 2015 and season_type = 'Regular' order by home_team;


print get_timezone('CAR')
print get_timezone('SEA')
print get_timezone('NE')


