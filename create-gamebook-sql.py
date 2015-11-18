import pandas as pd
df = pd.read_csv('output.csv')

string_cols = ['season_type', 'away_team', 'home_team', 'stadium', 'stadium_type', 'turf_type', 'away_qb_name', 'home_qb_name', 'away_time_of_possession', 'home_time_of_possession']
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
    if col in string_cols:
        sqltype = ' VARCHAR(40)'
    elif col in float_cols:
        sqltype = ' NUMERIC(6,2)'
    else:
        sqltype = ' INTEGER'
    line = "\t{}{}{}".format(col, sqltype, constraint)
    if i < len(all_cols) - 1:
        line += ','
    print line
print ");\n"
print "\copy gamebook FROM './output.csv' DELIMITER ',' CSV HEADER;"
