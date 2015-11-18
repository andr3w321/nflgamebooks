import pandas as pd
df = pd.read_csv('output.csv')

med_string_cols = ['season_type', 'away_team', 'home_team', 'stadium', 'stadium_type', 'turf_type', 'away_qb_name', 'home_qb_name', 'away_time_of_possession', 'home_time_of_possession', 'start_time', 'time_zone', 'wind_direction', 'wind_chill', 'game_length', 'last_updated', 'humidity']
long_string_cols = ['game_weather', 'windspeed', 'referee', 'umpire', 'line_judge', 'side_judge', 'back_judge', 'field_judge', 'head_linesman', 'replay_official']
long_long_string_cols = ['outdoor_weather']
float_cols = ['away_qb_rating', 'home_qb_rating', 'away_qb_yards_per_rush', 'home_qb_yards_per_rush', 'away_avg_punt', 'home_avg_punt', 'away_avg_gain_per_offensive_play', 'home_avg_gain_per_offensive_play', 'away_avg_gain_per_pass_play_incn_thrown_passing', 'home_avg_gain_per_pass_play_incn_thrown_passing', 'away_avg_gain_per_rushing_play', 'home_avg_gain_per_rushing_play', 'away_net_punting_avg', 'home_net_punting_avg']
all_cols = df.columns.values

print "DROP TABLE IF EXISTS gamebook;"
print "CREATE TABLE gamebook("
for i in range(0, len(all_cols)):
    col = all_cols[i]
    if col == 'gamekey':
        constraint = ' PRIMARY KEY'
    else:
        constraint = ''
    if col in med_string_cols:
        sqltype = ' VARCHAR(40)'
    elif col in long_string_cols:
        sqltype = ' VARCHAR(80)'
    elif col in long_long_string_cols:
        sqltype = ' VARCHAR(140)'
    elif col in float_cols:
        sqltype = ' NUMERIC(6,2)'
    elif col == 'schedule_date':
        sqltype = ' DATE'
    else:
        sqltype = ' INTEGER'
    line = "\t{}{}{}".format(col, sqltype, constraint)
    if i < len(all_cols) - 1:
        line += ','
    print line
print ");\n"
print "\copy gamebook FROM './output.csv' DELIMITER ',' CSV HEADER;"
