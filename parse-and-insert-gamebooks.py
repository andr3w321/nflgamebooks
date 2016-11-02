import os
import re
import sys
import xml.dom.minidom as xml
from nfldb import standard_team
from stadium import standard_stadium
import psycopg2

''' Sort the given list in the way that humans expect. '''
def sort_nicely( l ): 
  convert = lambda text: int(text) if text.isdigit() else text 
  alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
  l.sort( key=alphanum_key ) 

''' Removes periods and replaces spaces with _'''
def replace_periods_and_spaces(str):
    return str.replace(' ', '_').replace('.', '').replace('(','').replace(')','').replace('#','n').replace('average','avg')

''' Converts a short season_type to long season_type '''
def short_to_long_stype(stype):
    if stype == 'Reg':
        return 'Regular'
    elif stype == 'Pre':
        return 'Preseason'
    elif stype == 'Post':
        return 'Postseason'
    else:
        sys.stderr.write("Invalid season type: {}\n".format(stype))

'''
Returns a list of all filenames in a dir
that starts with a given string 
and ends with a given string
eg: get_filenames("./nfl-schedules", "1970", ".xml")
'''
def get_filenames(dir_path, starts_with, ends_with):
    filenames = []
    try:
        for file in os.listdir(dir_path):
            if file.startswith(starts_with) and file.endswith(ends_with):
                filenames.append(file)
    except OSError:
        sys.stderr.write("could not load %s\n" % dir_path)
    return filenames

''' A few gamebooks have blank stadium values.  Fill them in here. '''
def edge_case_stadium(gamekey):
    if gamekey == '17687':
        return 'Pro Player Stadium'
    if gamekey == '17752' or gamekey == '26336':
        return 'Georgia Dome'
    if gamekey == '17875' or gamekey == '26513' or gamekey == '18344' or gamekey == '26353':
        return 'RCA Dome'
    if gamekey == '26328' or gamekey == '26490':
        return 'Network Associates Coliseum'
    return ''

''' Given an xml_file, return the dom '''
def get_dom(gamebooks_path, xml_file):
    try:
        with open(gamebooks_path + '/' + xml_file, 'r') as f:
            content = f.read()
        # replace copyright symbol
        utf8_text = re.sub(u'[\u00a9\u24b8\u24d2]', '(c)', content)
        # replace extra > at end of one xml file
        utf8_text = re.sub('>>', '>', utf8_text)
        # replace random unicode strings
        utf8_text = unicode(utf8_text, errors='ignore')
        dom = xml.parseString(utf8_text)
        return dom
    except:
        sys.stderr.write("Error could not load %s\n" % xml_file)

''' Given an xml element and attribute name, return the attribute's string '''
def get_xml_attribute(elem, attr_name):
    return elem.getAttribute(attr_name).encode('utf-8')

''' Remove commas from a string and return it '''
def remove_commas(string_in):
    return re.sub(',', '', string_in)

''' Given an xml array of elements of players, parse them and return an array '''
def parse_players(elems):
    players = []
    for elem in elems:
        player = {}
        player['name'] = get_xml_attribute(elem, 'Player')
        player['position'] = get_xml_attribute(elem, 'Position')
        player['uniform_number'] = get_xml_attribute(elem, 'UniformNumber')
        player['last_name'] = get_xml_attribute(elem, 'LastName')
        player['nick_name'] = get_xml_attribute(elem, 'NickName')
        players.append(player)
    return players

def parse_players_from_xml(dom, elem_name):
    players_xml = dom.getElementsByTagName(elem_name)
    players = parse_players(players_xml)
    return players

def get_starting_position_player_name(players, position):
    for player in players:
        if player['position'] == position:
            return player['name']
    sys.stderr.write("Error: No player found with position %s\n" % (position))
    return ''


''' Helper function to find unique values for fields like stadium types '''
def save_and_print_new(value, values):
    if value not in values:
        values.append(value)
        print value

''' Given a QB name and array of passers_xml, returns a json object of that qbs stats for the game '''
def get_qb_stats(qb_name, passers_xml, rushers_xml):
    qb_stats = {'name': '', 'pass attempts': '', 'completions': '', 'pass yards': '', 'sacks': '', 'sack yardage': '', 'pass tds': '', 'long pass': '', 'interceptions': '', 'rating': '', 'rush attempts': '', 'rush yards': '', 'yards per rush': '', 'rush tds': '', 'long rush': ''}
    for passer_xml in passers_xml:
        player_name = get_xml_attribute(passer_xml, 'Player')
        # edge case, some starting qb position will be wrong so the qb_name will be blank, try assigning it
        if qb_name == '' and player_name != 'Total':
            qb_name = player_name
            sys.stderr.write("Error: blank QB name, using {}\n".format(qb_name))
        if player_name == qb_name:
            qb_stats['name'] = player_name
            qb_stats['pass attempts'] = get_xml_attribute(passer_xml, 'Attempts')
            qb_stats['completions'] = get_xml_attribute(passer_xml, 'Completions')
            qb_stats['pass yards'] = get_xml_attribute(passer_xml, 'Yards')
            qb_stats['sacks'] = get_xml_attribute(passer_xml, 'Sacks')
            qb_stats['sack yardage'] = get_xml_attribute(passer_xml, 'SackYardage')
            qb_stats['pass tds'] = get_xml_attribute(passer_xml, 'Touchdowns')
            qb_stats['long pass'] = re.sub('t', '', get_xml_attribute(passer_xml, 'Long'))
            qb_stats['interceptions'] = get_xml_attribute(passer_xml, 'Interceptions')
            qb_stats['rating'] = get_xml_attribute(passer_xml, 'Rating')
    for rusher_xml in rushers_xml:
        player_name = get_xml_attribute(rusher_xml, 'Player')
        if player_name == qb_name:
            qb_stats['rush attempts'] = get_xml_attribute(rusher_xml, 'Attempts')
            qb_stats['rush yards'] = get_xml_attribute(rusher_xml, 'Yards')
            qb_stats['yards per rush'] = get_xml_attribute(rusher_xml, 'Average')
            qb_stats['rush tds'] = get_xml_attribute(rusher_xml, 'Touchdowns')
            qb_stats['long rush'] = re.sub('t', '', get_xml_attribute(rusher_xml, 'Long'))
    # edge case, some starting qb names will be wrong, if at this point qb_name is still blank the original qb_name must have been wrong
    # try again using a blank qb_name
    if qb_stats['name'] == '':
        # warning can recursively loop forever
        sys.stderr.write("No qb stats found for {}\n".format(qb_name))
        return get_qb_stats('', passers_xml, rushers_xml)
    else:
        return qb_stats

''' Given an interceptor name and array of passers_xml, returns a json object of that incterceptors stats for the game '''
def get_interceptor_stats(interceptor_name, interceptors_xml):
    interceptor_stats = {}
    for interceptor_xml in interceptors_xml:
        player_name = get_xml_attribute(interceptor_xml, 'Player')
        if player_name == interceptor_name:
            interceptor_stats['Number'] = get_xml_attribute(interceptor_xml, 'Number')
            interceptor_stats['Yards'] = get_xml_attribute(interceptor_xml, 'Yards')
            interceptor_stats['Average'] = get_xml_attribute(interceptor_xml, 'Average')
            interceptor_stats['Long'] = get_xml_attribute(interceptor_xml, 'Long')
            interceptor_stats['Touchdowns'] = get_xml_attribute(interceptor_xml, 'Touchdowns')
    return interceptor_stats

''' Given an array, print each element out separated by commas as one line adding quotes if field contains a comma'''
def print_ary_as_csv_line(ary):
    line = ""
    for i in range(0, len(ary)):
        if ',' in ary[i]:
            line += "\"" + ary[i] + "\""
        else:
            line += ary[i]
        if i < len(ary) - 1:
            line += ","
    print line

''' Given the array of gamebook data, insert it into the db '''
def upsert_gamebook(output):
    # replace blank strings with None
    for i in range(0, len(output)):
        if output[i] == '':
            output[i] = None
    # unpack a few fields from output array
    season_year,week,season_type,gamekey = output[0], output[1], output[2], output[3]
    # select
    SQL = """SELECT season_year,week,season_type,gamekey,away_team,home_team,stadium,stadium_type,turf_type,schedule_date,start_time,time_zone,game_weather,temp,humidity,windspeed,outdoor_weather,wind_chill,wind_direction,referee,umpire,head_linesman,line_judge,side_judge,back_judge,field_judge,replay_official,attendance,game_length,visitor_score_q1,visitor_score_q2,visitor_score_q3,visitor_score_q4,visitor_score_ot,home_score_q1,home_score_q2,home_score_q3,home_score_q4,home_score_ot,last_updated,away_qb_name,home_qb_name,away_qb_pass_attempts,home_qb_pass_attempts,away_qb_completions,home_qb_completions,away_qb_pass_yards,home_qb_pass_yards,away_qb_sacks,home_qb_sacks,away_qb_sack_yardage,home_qb_sack_yardage,away_qb_pass_tds,home_qb_pass_tds,away_qb_long_pass,home_qb_long_pass,away_qb_interceptions,home_qb_interceptions,away_qb_rating,home_qb_rating,away_qb_rush_attempts,home_qb_rush_attempts,away_qb_rush_yards,home_qb_rush_yards,away_qb_yards_per_rush,home_qb_yards_per_rush,away_qb_rush_tds,home_qb_rush_tds,away_qb_long_rush,home_qb_long_rush,away_third_downs_converted,home_third_downs_converted,away_third_downs,home_third_downs,away_third_down_convert_percent,home_third_down_convert_percent,away_fourth_downs_converted,home_fourth_downs_converted,away_fourth_downs,home_fourth_downs,away_fourth_down_convert_percent,home_fourth_down_convert_percent,away_tackles_for_a_loss,home_tackles_for_a_loss,away_tackles_for_a_loss_yardage,home_tackles_for_a_loss_yardage,away_times_thrown_yards_lost,home_times_thrown_yards_lost,away_yards_lost_attempting_to_pass,home_yards_lost_attempting_to_pass,away_pass_attempts,home_pass_attempts,away_completions,home_completions,away_had_intercepted,home_had_intercepted,away_n_kickoffs,home_n_kickoffs,away_n_kickoffs_in_endzone,home_n_kickoffs_in_endzone,away_n_kickoffs_touchbacks,home_n_kickoffs_touchbacks,away_n_punts,home_n_punts,away_avg_punt,home_avg_punt,away_fgs_had_blocked,home_fgs_had_blocked,away_pats_had_blocked,home_pats_had_blocked,away_n_punt_returns,home_n_punt_returns,away_yards_punt_returns,home_yards_punt_returns,away_n_kickoff_returns,home_n_kickoff_returns,away_yards_kickoff_returns,home_yards_kickoff_returns,away_n_interception_returns,home_n_interception_returns,away_yards_interception_returns,home_yards_interception_returns,away_n_penalties,home_n_penalties,away_penalty_yards,home_penalty_yards,away_n_fumbles,home_n_fumbles,away_n_fumbles_lost,home_n_fumbles_lost,away_extra_points_made,home_extra_points_made,away_extra_points_attempts,home_extra_points_attempts,away_kicking_made,home_kicking_made,away_kicking_attempts,home_kicking_attempts,away_field_goals_made,home_field_goals_made,away_field_goals_attempts,home_field_goals_attempts,away_red_zone_converts,home_red_zone_converts,away_red_zone_attempts,home_red_zone_attempts,away_red_zone_convert_percentage,home_red_zone_convert_percentage,away_goal_to_go_converts,home_goal_to_go_converts,away_goal_to_go_attempts,home_goal_to_go_attempts,away_goal_to_go_convert_percentage,home_goal_to_go_convert_percentage,away_time_of_possession,home_time_of_possession,away_total_first_downs,home_total_first_downs,away_first_downs_by_rushing,home_first_downs_by_rushing,away_first_downs_by_passing,home_first_downs_by_passing,away_first_downs_by_penalty,home_first_downs_by_penalty,away_total_net_yards,home_total_net_yards,away_total_offensive_plays_inc_times_thrown_passing,home_total_offensive_plays_inc_times_thrown_passing,away_avg_gain_per_offensive_play,home_avg_gain_per_offensive_play,away_net_yards_rushing,home_net_yards_rushing,away_total_rushing_plays,home_total_rushing_plays,away_avg_gain_per_rushing_play,home_avg_gain_per_rushing_play,away_net_yards_passing,home_net_yards_passing,away_gross_yards_passing,home_gross_yards_passing,away_avg_gain_per_pass_play_incn_thrown_passing,home_avg_gain_per_pass_play_incn_thrown_passing,away_had_blocked,home_had_blocked,away_net_punting_avg,home_net_punting_avg,away_total_return_yardage_not_including_kickoffs,home_total_return_yardage_not_including_kickoffs,away_touchdowns,home_touchdowns,away_tds_by_rushing,home_tds_by_rushing,away_tds_by_passing,home_tds_by_passing,away_safeties,home_safeties,away_final_score,home_final_score,away_tds_by_fumbles,home_tds_by_fumbles,away_tds_by_interceptions,home_tds_by_interceptions,away_tds_by_punt_returns,home_tds_by_punt_returns,away_tds_by_kickoff_returns,home_tds_by_kickoff_returns,away_tds_by_other_blocked_kicks_etc,home_tds_by_other_blocked_kicks_etc,away_2pt_conv_rush_made,away_2pt_conv_rush_att,away_2pt_conv_pass_made,away_2pt_conv_pass_att,home_2pt_conv_rush_made,home_2pt_conv_rush_att,home_2pt_conv_pass_made,home_2pt_conv_pass_att FROM gamebook WHERE season_year = %s AND week = %s AND season_type = %s AND gamekey = %s;"""
    data = (season_year, week, season_type, gamekey)
    cur.execute(SQL, data)
    db_output = cur.fetchone()
    # delete old
    if db_output != None:
        SQL = """DELETE FROM gamebook WHERE season_year = %s AND week = %s AND season_type = %s AND gamekey = %s;"""
        data = (season_year, week, season_type, gamekey)
        cur.execute(SQL, data)
        #sys.stderr.write("DELETING {} gamebook {}-{}-{}-{} from db\n".format(cur.rowcount, season_year, week, season_type, gamekey))
    # insert new
    SQL = """INSERT INTO gamebook(season_year,week,season_type,gamekey,away_team,home_team,stadium,stadium_type,turf_type,schedule_date,start_time,time_zone,game_weather,temp,humidity,windspeed,outdoor_weather,wind_chill,wind_direction,referee,umpire,head_linesman,line_judge,side_judge,back_judge,field_judge,replay_official,attendance,game_length,visitor_score_q1,visitor_score_q2,visitor_score_q3,visitor_score_q4,visitor_score_ot,home_score_q1,home_score_q2,home_score_q3,home_score_q4,home_score_ot,last_updated,away_qb_name,home_qb_name,away_qb_pass_attempts,home_qb_pass_attempts,away_qb_completions,home_qb_completions,away_qb_pass_yards,home_qb_pass_yards,away_qb_sacks,home_qb_sacks,away_qb_sack_yardage,home_qb_sack_yardage,away_qb_pass_tds,home_qb_pass_tds,away_qb_long_pass,home_qb_long_pass,away_qb_interceptions,home_qb_interceptions,away_qb_rating,home_qb_rating,away_qb_rush_attempts,home_qb_rush_attempts,away_qb_rush_yards,home_qb_rush_yards,away_qb_yards_per_rush,home_qb_yards_per_rush,away_qb_rush_tds,home_qb_rush_tds,away_qb_long_rush,home_qb_long_rush,away_third_downs_converted,home_third_downs_converted,away_third_downs,home_third_downs,away_third_down_convert_percent,home_third_down_convert_percent,away_fourth_downs_converted,home_fourth_downs_converted,away_fourth_downs,home_fourth_downs,away_fourth_down_convert_percent,home_fourth_down_convert_percent,away_tackles_for_a_loss,home_tackles_for_a_loss,away_tackles_for_a_loss_yardage,home_tackles_for_a_loss_yardage,away_times_thrown_yards_lost,home_times_thrown_yards_lost,away_yards_lost_attempting_to_pass,home_yards_lost_attempting_to_pass,away_pass_attempts,home_pass_attempts,away_completions,home_completions,away_had_intercepted,home_had_intercepted,away_n_kickoffs,home_n_kickoffs,away_n_kickoffs_in_endzone,home_n_kickoffs_in_endzone,away_n_kickoffs_touchbacks,home_n_kickoffs_touchbacks,away_n_punts,home_n_punts,away_avg_punt,home_avg_punt,away_fgs_had_blocked,home_fgs_had_blocked,away_pats_had_blocked,home_pats_had_blocked,away_n_punt_returns,home_n_punt_returns,away_yards_punt_returns,home_yards_punt_returns,away_n_kickoff_returns,home_n_kickoff_returns,away_yards_kickoff_returns,home_yards_kickoff_returns,away_n_interception_returns,home_n_interception_returns,away_yards_interception_returns,home_yards_interception_returns,away_n_penalties,home_n_penalties,away_penalty_yards,home_penalty_yards,away_n_fumbles,home_n_fumbles,away_n_fumbles_lost,home_n_fumbles_lost,away_extra_points_made,home_extra_points_made,away_extra_points_attempts,home_extra_points_attempts,away_kicking_made,home_kicking_made,away_kicking_attempts,home_kicking_attempts,away_field_goals_made,home_field_goals_made,away_field_goals_attempts,home_field_goals_attempts,away_red_zone_converts,home_red_zone_converts,away_red_zone_attempts,home_red_zone_attempts,away_red_zone_convert_percentage,home_red_zone_convert_percentage,away_goal_to_go_converts,home_goal_to_go_converts,away_goal_to_go_attempts,home_goal_to_go_attempts,away_goal_to_go_convert_percentage,home_goal_to_go_convert_percentage,away_time_of_possession,home_time_of_possession,away_total_first_downs,home_total_first_downs,away_first_downs_by_rushing,home_first_downs_by_rushing,away_first_downs_by_passing,home_first_downs_by_passing,away_first_downs_by_penalty,home_first_downs_by_penalty,away_total_net_yards,home_total_net_yards,away_total_offensive_plays_inc_times_thrown_passing,home_total_offensive_plays_inc_times_thrown_passing,away_avg_gain_per_offensive_play,home_avg_gain_per_offensive_play,away_net_yards_rushing,home_net_yards_rushing,away_total_rushing_plays,home_total_rushing_plays,away_avg_gain_per_rushing_play,home_avg_gain_per_rushing_play,away_net_yards_passing,home_net_yards_passing,away_gross_yards_passing,home_gross_yards_passing,away_avg_gain_per_pass_play_incn_thrown_passing,home_avg_gain_per_pass_play_incn_thrown_passing,away_had_blocked,home_had_blocked,away_net_punting_avg,home_net_punting_avg,away_total_return_yardage_not_including_kickoffs,home_total_return_yardage_not_including_kickoffs,away_touchdowns,home_touchdowns,away_tds_by_rushing,home_tds_by_rushing,away_tds_by_passing,home_tds_by_passing,away_safeties,home_safeties,away_final_score,home_final_score,away_tds_by_fumbles,home_tds_by_fumbles,away_tds_by_interceptions,home_tds_by_interceptions,away_tds_by_punt_returns,home_tds_by_punt_returns,away_tds_by_kickoff_returns,home_tds_by_kickoff_returns,away_tds_by_other_blocked_kicks_etc,home_tds_by_other_blocked_kicks_etc,away_2pt_conv_rush_made,away_2pt_conv_rush_att,away_2pt_conv_pass_made,away_2pt_conv_pass_att,home_2pt_conv_rush_made,home_2pt_conv_rush_att,home_2pt_conv_pass_made,home_2pt_conv_pass_att) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    data = (tuple(output))
    cur.execute(SQL, data)
    #sys.stderr.write("INSERTING {} gamebook {}-{}-{}-{} from db\n".format(cur.rowcount, season_year, week, season_type, gamekey))

''' Given a list of dom drive elements, parse out the attributes and insert them into the db '''
def parse_and_upsert_drives(gamekey, drives_dom, is_away_team, away_team, home_team):
    drives_inserted = 0
    # set possessing team
    if is_away_team == True:
        pos_team = away_team
    else:
        pos_team = home_team

    # parse drive attributes
    for drive in drives_dom:
        drive_n = get_xml_attribute(drive, 'Number')
        quarter = get_xml_attribute(drive, 'Quarter')
        time_received = get_xml_attribute(drive, 'TimeReceived')
        time_lost = get_xml_attribute(drive, 'TimeLost')
        time_of_pos = get_xml_attribute(drive, 'TimeOfPossession')
        # convert time of possession to an integer of seconds
        pos_minutes, pos_seconds = [int(i) for i in time_of_pos.split(':')]
        pos_time = pos_minutes * 60 + pos_seconds
        how_ball_obtained = get_xml_attribute(drive, 'HowBallObtained')
        # convert drive began to start field between -49 to +49
        drive_began = get_xml_attribute(drive, 'DriveBegan')
        # edge cases with strange team abbrev in drive charts
        drive_began = drive_began.replace("BLT", "BAL")
        drive_began = drive_began.replace("JAX", "JAC")
        drive_began = drive_began.replace("SL", "STL")
        drive_began = drive_began.replace("CLV", "CLE")
        drive_began = drive_began.replace("ARZ", "ARI")
        drive_began = drive_began.replace("HST", "HOU")
        if away_team in drive_began or home_team in drive_began:
            start_field = 50 - int(drive_began.split(' ')[1])
            if (away_team in drive_began and is_away_team == True) or (home_team in drive_began and is_away_team == False):
                start_field = start_field * -1
        elif drive_began == "50":
            start_field = 0
        elif drive_began == "":
            # sometimes a fumble on kickoff
            start_field = None
        else:
            sys.stderr.write("ERROR in drive {} can't find start_field for {}\n".format(drive_n, drive_began))

        play_count = get_xml_attribute(drive, 'PlayCount')
        yards_gained = get_xml_attribute(drive, 'YardsGained')
        yards_penalized = get_xml_attribute(drive, 'YardsPenalized')
        net_yards = get_xml_attribute(drive, 'NetYards')
        first_downs = get_xml_attribute(drive, 'FirstDowns')
        result = get_xml_attribute(drive, 'HowGivenUp')

        # delete drive if already found in db
        SQL = """DELETE FROM gamebook_drive WHERE gamekey = %s AND pos_team = %s AND drive_n = %s;"""
        data = (gamekey, pos_team, drive_n)
        cur.execute(SQL, data)

        # insert drive
        SQL = """INSERT INTO gamebook_drive(gamekey, pos_team, drive_n, quarter, time_received, time_lost, pos_time, how_ball_obtained, start_field, play_count, yards_gained, yards_penalized, net_yards, first_downs, result) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = (gamekey, pos_team, drive_n, quarter, time_received, time_lost, pos_time, how_ball_obtained, start_field, play_count, yards_gained, yards_penalized, net_yards, first_downs, result)
        cur.execute(SQL, data)
        drives_inserted += cur.rowcount
    return drives_inserted

''' Given a list of xml filenames for gamebooks, parse out the data, then insert it into db '''
def parse_upsert_xmls(xml_filenames, qb_stat_descs, stat_descs, stat_with_dash_descs, rare_stat_descs, rare_stat_with_dash_descs):
    for xml_file in xml_filenames:
        # raw game summary data
        season_year,week,season_type,gamekey = xml_file.split('.xml')[0].split('-')
        sys.stderr.write("{}-{}-{}-{}.xml\n".format(season_year, week, season_type, gamekey))
        season_type = short_to_long_stype(season_type)
        dom = get_dom(gamebooks_path, xml_file)
        gamebook_summary = dom.getElementsByTagName('GamebookSummary')[0]
        schedule_date = get_xml_attribute(gamebook_summary, 'ScheduleDate')
        home_team = get_xml_attribute(gamebook_summary, 'HomeTeam')
        away_team = get_xml_attribute(gamebook_summary, 'VisitingTeam')
        start_time = get_xml_attribute(gamebook_summary, 'StartTime')
        time_zone = get_xml_attribute(gamebook_summary, 'TimeZone')
        stadium = get_xml_attribute(gamebook_summary, 'Stadium')
        stadium_type = get_xml_attribute(gamebook_summary, 'StadiumType')
        game_weather = get_xml_attribute(gamebook_summary, 'GameWeather')
        temp = get_xml_attribute(gamebook_summary, 'Temperature')
        humidity = get_xml_attribute(gamebook_summary, 'Humidity')
        windspeed = get_xml_attribute(gamebook_summary, 'WindSpeed')
        turf_type = get_xml_attribute(gamebook_summary, 'TurfType')
        outdoor_weather = get_xml_attribute(gamebook_summary, 'OutdoorWeather')
        wind_chill = get_xml_attribute(gamebook_summary, 'WindChill')
        wind_direction = get_xml_attribute(gamebook_summary, 'WindDirection')
        referee = get_xml_attribute(gamebook_summary, 'Referee')
        umpire = get_xml_attribute(gamebook_summary, 'Umpire')
        head_linesman = get_xml_attribute(gamebook_summary, 'HeadLinesman')
        line_judge = get_xml_attribute(gamebook_summary, 'LineJudge')
        side_judge = get_xml_attribute(gamebook_summary, 'SideJudge')
        back_judge = get_xml_attribute(gamebook_summary, 'BackJudge')
        field_judge = get_xml_attribute(gamebook_summary, 'FieldJudge')
        replay_official = get_xml_attribute(gamebook_summary, 'ReplayOfficial')
        attendance = get_xml_attribute(gamebook_summary, 'Attendance').replace(',','')
        game_length = get_xml_attribute(gamebook_summary, 'GameLength')
        visitor_score_q1 = get_xml_attribute(gamebook_summary, 'VisitorScoreQ1')
        visitor_score_q2 = get_xml_attribute(gamebook_summary, 'VisitorScoreQ2')
        visitor_score_q3 = get_xml_attribute(gamebook_summary, 'VisitorScoreQ3')
        visitor_score_q4 = get_xml_attribute(gamebook_summary, 'VisitorScoreQ4')
        visitor_score_ot = get_xml_attribute(gamebook_summary, 'VisitorScoreOT')
        home_score_q1 = get_xml_attribute(gamebook_summary, 'HomeScoreQ1')
        home_score_q2 = get_xml_attribute(gamebook_summary, 'HomeScoreQ2')
        home_score_q3 = get_xml_attribute(gamebook_summary, 'HomeScoreQ3')
        home_score_q4 = get_xml_attribute(gamebook_summary, 'HomeScoreQ4')
        home_score_ot = get_xml_attribute(gamebook_summary, 'HomeScoreOT')
        last_updated = get_xml_attribute(gamebook_summary, 'LastUpdated')
        
        # raw roster data
        offensive_starters_away = parse_players_from_xml(dom, 'OffensiveStarterVisitor')
        offensive_starters_home = parse_players_from_xml(dom, 'OffensiveStarterHome')
        defensive_starters_away = parse_players_from_xml(dom, 'DefensiveStarterVisitor')
        defensive_starters_home = parse_players_from_xml(dom, 'DefensiveStarterHome')
        subs_away = parse_players_from_xml(dom, 'SubstitutionsVisitor')
        subs_home = parse_players_from_xml(dom, 'SubstitutionsHome')
        did_not_play_away = parse_players_from_xml(dom, 'DidNotPlayVisitor')
        did_not_play_home = parse_players_from_xml(dom, 'DidNotPlayHome')
        not_active_away = parse_players_from_xml(dom, 'NotActiveVisitor')
        not_active_home = parse_players_from_xml(dom, 'NotActiveHome')

        # raw team statistics
        all_team_stats_xml = dom.getElementsByTagName('TeamStatistics')
        first_half_team_stats_xml = dom.getElementsByTagName('FirstHalfSummary')[0].getElementsByTagName('TeamStatistics')
        # filter out first half stats to get just the full game team stats
        game_team_stats_xml = []
        for team_stat_xml in all_team_stats_xml:
            if team_stat_xml not in first_half_team_stats_xml:
                game_team_stats_xml.append(team_stat_xml)
        home_team_stats = {}
        away_team_stats = {}
        for team_stat_xml in game_team_stats_xml:
            # convert all descriptions to lowercase
            team_stat_description = get_xml_attribute(team_stat_xml, 'Description').lower()
            # edge case error, replace all double -- with single -
            away_team_stats[team_stat_description] = re.sub('--', '-', get_xml_attribute(team_stat_xml, 'VisitorStats'))
            home_team_stats[team_stat_description] = re.sub('--', '-', get_xml_attribute(team_stat_xml, 'HomeStats'))

            # check for unknown stats
            if team_stat_description not in stat_descs and \
                    team_stat_description not in stat_with_dash_descs and \
                    team_stat_description not in rare_stat_descs and \
                    team_stat_description not in rare_stat_with_dash_descs:
                print "ERROR: Unknown team stat %s" % team_stat_description

        # clean and standardize the raw game summary data
        home_team = standard_team(home_team)
        away_team = standard_team(away_team)
        # some stadium values are empty, manually replace each one
        if stadium == '':
            stadium = edge_case_stadium(gamekey)
        stadium = standard_stadium(stadium)

        # split up the team stats with dash
        away_team_stats['third downs converted'], away_team_stats['third downs'], away_team_stats['third down convert percent'] = re.sub('%', '', away_team_stats['third down efficiency']).split('-')
        home_team_stats['third downs converted'], home_team_stats['third downs'], home_team_stats['third down convert percent'] = re.sub('%', '', home_team_stats['third down efficiency']).split('-')
        away_team_stats['fourth downs converted'], away_team_stats['fourth downs'], away_team_stats['fourth down convert percent'] = re.sub('%', '', away_team_stats['fourth down efficiency']).split('-')
        home_team_stats['fourth downs converted'], home_team_stats['fourth downs'], home_team_stats['fourth down convert percent'] = re.sub('%', '', home_team_stats['fourth down efficiency']).split('-')
        away_team_stats['tackles for a loss'], away_team_stats['tackles for a loss yardage'] = away_team_stats['tackles for a loss-number and yards'].split('-')
        home_team_stats['tackles for a loss'], home_team_stats['tackles for a loss yardage'] = home_team_stats['tackles for a loss-number and yards'].split('-')
        away_team_stats['times thrown'], away_team_stats['yards lost attempting to pass'] = away_team_stats['times thrown - yards lost attempting to pass'].split('-')
        home_team_stats['times thrown'], home_team_stats['yards lost attempting to pass'] = home_team_stats['times thrown - yards lost attempting to pass'].split('-')
        away_team_stats['pass attempts'], away_team_stats['completions'], away_team_stats['had intercepted'] = away_team_stats['pass attempts-completions-had intercepted'].split('-')
        home_team_stats['pass attempts'], home_team_stats['completions'], home_team_stats['had intercepted'] = home_team_stats['pass attempts-completions-had intercepted'].split('-')
        away_team_stats['n kickoffs'], away_team_stats['n kickoffs in endzone'], away_team_stats['n kickoffs touchbacks'] = away_team_stats['kickoffs number-in end zone-touchbacks'].split('-')
        home_team_stats['n kickoffs'], home_team_stats['n kickoffs in endzone'], home_team_stats['n kickoffs touchbacks'] = home_team_stats['kickoffs number-in end zone-touchbacks'].split('-')
        away_team_stats['n punts'], away_team_stats['avg punt'] = away_team_stats['punts number and average'].split('-')
        home_team_stats['n punts'], home_team_stats['avg punt'] = home_team_stats['punts number and average'].split('-')
        away_team_stats['fgs had blocked'], away_team_stats['pats had blocked'] = away_team_stats['fgs - pats had blocked'].split('-')
        home_team_stats['fgs had blocked'], home_team_stats['pats had blocked'] = home_team_stats['fgs - pats had blocked'].split('-')
        away_team_stats['n punt returns'], away_team_stats['yards punt returns'] = away_team_stats['no. and yards punt returns'].split('-')
        home_team_stats['n punt returns'], home_team_stats['yards punt returns'] = home_team_stats['no. and yards punt returns'].split('-')
        away_team_stats['n kickoff returns'], away_team_stats['yards kickoff returns'] = away_team_stats['no. and yards kickoff returns'].split('-')
        home_team_stats['n kickoff returns'], home_team_stats['yards kickoff returns'] = home_team_stats['no. and yards kickoff returns'].split('-')
        away_team_stats['n interception returns'], away_team_stats['yards interception returns'] = away_team_stats['no. and yards interception returns'].split('-')
        home_team_stats['n interception returns'], home_team_stats['yards interception returns'] = home_team_stats['no. and yards interception returns'].split('-')
        away_team_stats['n penalties'], away_team_stats['penalty yards'] = away_team_stats['penalties number and yards'].split('-')
        home_team_stats['n penalties'], home_team_stats['penalty yards'] = home_team_stats['penalties number and yards'].split('-')
        away_team_stats['n fumbles'], away_team_stats['n fumbles lost'] = away_team_stats['fumbles number and lost'].split('-')
        home_team_stats['n fumbles'], home_team_stats['n fumbles lost'] = home_team_stats['fumbles number and lost'].split('-')
        away_team_stats['extra points made'], away_team_stats['extra points attempts'] = away_team_stats['extra points made-attempts'].split('-')
        home_team_stats['extra points made'], home_team_stats['extra points attempts'] = home_team_stats['extra points made-attempts'].split('-')
        away_team_stats['kicking made'], away_team_stats['kicking attempts'] = away_team_stats['kicking made-attempts'].split('-')
        home_team_stats['kicking made'], home_team_stats['kicking attempts'] = home_team_stats['kicking made-attempts'].split('-')
        away_team_stats['field goals made'], away_team_stats['field goals attempts'] = away_team_stats['field goals made-attempts'].split('-')
        home_team_stats['field goals made'], home_team_stats['field goals attempts'] = home_team_stats['field goals made-attempts'].split('-')
        away_team_stats['red zone converts'], away_team_stats['red zone attempts'], away_team_stats['red zone convert percentage'] = re.sub('%', '', away_team_stats['red zone efficiency']).split('-')
        home_team_stats['red zone converts'], home_team_stats['red zone attempts'], home_team_stats['red zone convert percentage'] = re.sub('%', '', home_team_stats['red zone efficiency']).split('-')
        away_team_stats['goal to go converts'], away_team_stats['goal to go attempts'], away_team_stats['goal to go convert percentage'] = re.sub('%', '', away_team_stats['goal to go efficiency']).split('-')
        home_team_stats['goal to go converts'], home_team_stats['goal to go attempts'], home_team_stats['goal to go convert percentage'] = re.sub('%', '', home_team_stats['goal to go efficiency']).split('-')
        '''
        away_team_stats['time of possession minutes'], away_team_stats['time of possession seconds'] = away_team_stats['time of possession'].split(':')
        home_team_stats['time of possession minutes'], home_team_stats['time of possession seconds'] = home_team_stats['time of possession'].split(':')
        away_team_stats['time of possession decimal'] = str(round(float(away_team_stats['time of possession minutes']) + float(away_team_stats['time of possession seconds']) / 60.0, 2))
        home_team_stats['time of possession decimal'] = str(round(float(home_team_stats['time of possession minutes']) + float(home_team_stats['time of possession seconds']) / 60.0, 2))
        '''

        # set rare team stats to zero if they don't exist
        for rare_stat_desc in rare_stat_descs:
            if rare_stat_desc not in away_team_stats:
                away_team_stats[rare_stat_desc] = '0'
                home_team_stats[rare_stat_desc] = '0'

        # set rare team stats with dash to zero if they don't exist, fill them in otherwise
        if 'rushing made-attempts' in away_team_stats:
            away_team_stats['2pt conv rush made'] = away_team_stats['rushing made-attempts'].split('-')[0]
            away_team_stats['2pt conv rush att'] = away_team_stats['rushing made-attempts'].split('-')[1]
            home_team_stats['2pt conv rush made'] = home_team_stats['rushing made-attempts'].split('-')[0]
            home_team_stats['2pt conv rush att'] = home_team_stats['rushing made-attempts'].split('-')[1]
        else:
            away_team_stats['2pt conv rush made'] = '0'
            away_team_stats['2pt conv rush att'] = '0'
            home_team_stats['2pt conv rush made'] = '0'
            home_team_stats['2pt conv rush att'] = '0'
        if 'passing made-attempts' in away_team_stats:
            away_team_stats['2pt conv pass made'] = away_team_stats['passing made-attempts'].split('-')[0]
            away_team_stats['2pt conv pass att'] = away_team_stats['passing made-attempts'].split('-')[1]
            home_team_stats['2pt conv pass made'] = home_team_stats['passing made-attempts'].split('-')[0]
            home_team_stats['2pt conv pass att'] = home_team_stats['passing made-attempts'].split('-')[1]
        else:
            away_team_stats['2pt conv pass made'] = '0'
            away_team_stats['2pt conv pass att'] = '0'
            home_team_stats['2pt conv pass made'] = '0'
            home_team_stats['2pt conv pass att'] = '0'

        # raw individual stats
        individual_stats_dom = dom.getElementsByTagName('IndividualStatistics')[0]

        # get starting qbs names
        starting_qb_away_name = get_starting_position_player_name(offensive_starters_away, 'QB')
        starting_qb_home_name = get_starting_position_player_name(offensive_starters_home, 'QB')

        # get qb stats for away starter and for the game
        away_passers_xml = individual_stats_dom.getElementsByTagName('PasserVisitor')
        away_rushers_xml = individual_stats_dom.getElementsByTagName('RusherVisitor')
        away_qb_stats = get_qb_stats(starting_qb_away_name, away_passers_xml, away_rushers_xml)
        away_total_qb_stats = get_qb_stats('Total', away_passers_xml, away_rushers_xml)

        # get qb stats for home starter and for the game
        home_passers_xml = individual_stats_dom.getElementsByTagName('PasserHome')
        home_rushers_xml = individual_stats_dom.getElementsByTagName('RusherHome')
        home_qb_stats = get_qb_stats(starting_qb_home_name, home_passers_xml, home_rushers_xml)
        home_total_qb_stats = get_qb_stats('Total', home_passers_xml, home_rushers_xml)

        # get away interceptors stats
        away_interceptors_xml = individual_stats_dom.getElementsByTagName('InterceptorVisitor')
        away_interceptor_stats = get_interceptor_stats('Total', away_interceptors_xml)

        # get home interceptors stats
        home_interceptors_xml = individual_stats_dom.getElementsByTagName('InterceptorHome')
        home_interceptor_stats = get_interceptor_stats('Total', home_interceptors_xml)

        output = [season_year,week,season_type,gamekey,away_team,home_team,stadium,stadium_type,turf_type,schedule_date,start_time,time_zone,game_weather,temp,humidity,windspeed,outdoor_weather,wind_chill,wind_direction,referee,umpire,head_linesman,line_judge,side_judge,back_judge,field_judge,replay_official,attendance,game_length,visitor_score_q1,visitor_score_q2,visitor_score_q3,visitor_score_q4,visitor_score_ot,home_score_q1,home_score_q2,home_score_q3,home_score_q4,home_score_ot,last_updated]
        for qb_stat in qb_stat_descs:
            output.append(away_qb_stats[qb_stat])
            output.append(home_qb_stats[qb_stat])

        for stat in stat_descs + rare_stat_descs:
            output.append(away_team_stats[stat])
            output.append(home_team_stats[stat])
        output += [away_team_stats['2pt conv rush made'], away_team_stats['2pt conv rush att'], away_team_stats['2pt conv pass made'], away_team_stats['2pt conv pass att']]
        output += [home_team_stats['2pt conv rush made'], home_team_stats['2pt conv rush att'], home_team_stats['2pt conv pass made'], home_team_stats['2pt conv pass att']]

        # upsert gamebooks
        upsert_gamebook(output)

        # parse and upsert gamebook drives
        away_drive_stats_dom = dom.getElementsByTagName('DriveVisitor')
        home_drive_stats_dom = dom.getElementsByTagName('DriveHome')
        away_drives_inserted = parse_and_upsert_drives(gamekey, away_drive_stats_dom, True, away_team, home_team)
        home_drives_inserted = parse_and_upsert_drives(gamekey, home_drive_stats_dom, False, away_team, home_team)
        #print "{} away and {} home drives inserted".format(away_drives_inserted, home_drives_inserted)


###Compile the sql column names as a csv
qb_stat_descs = ['name', 'pass attempts', 'completions', 'pass yards', 'sacks', 'sack yardage', 'pass tds', 'long pass', 'interceptions', 'rating', 'rush attempts', 'rush yards', 'yards per rush', 'rush tds', 'long rush']
stat_descs = ['third downs converted', 'third downs', 'third down convert percent', 'fourth downs converted', 'fourth downs', 'fourth down convert percent', 'tackles for a loss', 'tackles for a loss yardage', 'times thrown', 'yards lost attempting to pass', 'pass attempts', 'completions', 'had intercepted', 'n kickoffs', 'n kickoffs in endzone', 'n kickoffs touchbacks', 'n punts', 'avg punt', 'fgs had blocked', 'pats had blocked', 'n punt returns', 'yards punt returns', 'n kickoff returns', 'yards kickoff returns', 'n interception returns', 'yards interception returns', 'n penalties', 'penalty yards', 'n fumbles', 'n fumbles lost', 'extra points made', 'extra points attempts', 'kicking made', 'kicking attempts', 'field goals made', 'field goals attempts', 'red zone converts', 'red zone attempts', 'red zone convert percentage', 'goal to go converts', 'goal to go attempts', 'goal to go convert percentage', 'time of possession', 'total first downs', 'by rushing', 'by passing', 'by penalty', 'total net yards', 'total offensive plays (inc. times thrown passing)', 'average gain per offensive play', 'net yards rushing', 'total rushing plays', 'average gain per rushing play', 'net yards passing', 'gross yards passing', 'avg gain per pass play (inc.# thrown passing)', 'had blocked', 'net punting average', 'total return yardage (not including kickoffs)', 'touchdowns', 'rushing', 'passing', 'safeties', 'final score']
stat_with_dash_descs = ['third down efficiency', 'fourth down efficiency', 'tackles for a loss-number and yards', 'times thrown - yards lost attempting to pass', 'pass attempts-completions-had intercepted', 'kickoffs number-in end zone-touchbacks', 'punts number and average', 'fgs - pats had blocked', 'no. and yards punt returns', 'no. and yards kickoff returns', 'no. and yards interception returns', 'penalties number and yards', 'fumbles number and lost', 'extra points made-attempts', 'kicking made-attempts', 'field goals made-attempts', 'red zone efficiency', 'goal to go efficiency']
rare_stat_descs = ['fumbles', 'interceptions', 'punt returns', 'kickoff returns', 'other (blocked kicks, etc.)']
rare_stat_with_dash_descs = ['rushing made-attempts', 'passing made-attempts']

# print the column names
header = "season_year,week,season_type,gamekey,away_team,home_team,stadium,stadium_type,turf_type,schedule_date,start_time,time_zone,game_weather,temp,humidity,windspeed,outdoor_weather,wind_chill,wind_direction,referee,umpire,head_linesman,line_judge,side_judge,back_judge,field_judge,replay_official,attendance,game_length,visitor_score_q1,visitor_score_q2,visitor_score_q3,visitor_score_q4,visitor_score_ot,home_score_q1,home_score_q2,home_score_q3,home_score_q4,home_score_ot,last_updated"
for qb_stat in qb_stat_descs:
    header += ",away_qb_" + replace_periods_and_spaces(qb_stat)
    header += ",home_qb_" + replace_periods_and_spaces(qb_stat)
for stat in stat_descs + rare_stat_descs:
    if stat == 'by passing' or stat == 'by rushing' or stat == 'by penalty':
        stat = 'first_downs_' + stat
    # remove comma from blocked kicks field prepend tds_by
    if stat == "other (blocked kicks, etc.)":
        stat = "tds_by_other_blocked_kicks_etc"
    if stat == 'rushing' or stat == 'passing' or stat == 'fumbles' or stat == 'interceptions' or stat == 'punt returns' or stat == 'kickoff returns':
        stat = 'tds_by_' + stat
    if stat == 'times thrown':
        stat = 'times_thrown_yards_lost'
    header += ",away_" + replace_periods_and_spaces(stat)
    header += ",home_" + replace_periods_and_spaces(stat)
header += ',away_2pt_conv_rush_made,away_2pt_conv_rush_att,away_2pt_conv_pass_made,away_2pt_conv_pass_att'
header += ',home_2pt_conv_rush_made,home_2pt_conv_rush_att,home_2pt_conv_pass_made,home_2pt_conv_pass_att'
#print header

### DB connect
try:
    conn = psycopg2.connect("host=localhost dbname=nfldb user=nfldb")
except:
    print "I am unable to connect to the datbase."
cur = conn.cursor()

### Begin parsing the gamebooks
# get gamebook filenames in a sorted list
gamebooks_path = './gamebook-xml'
#xml_filenames = get_filenames(gamebooks_path, "2015-08-Reg-56621", ".xml")
#years = range(2002, 2016)
years = [2016]
for year in years:
    xml_filenames = get_filenames(gamebooks_path, str(year) + "-08-Reg", ".xml")
    sort_nicely(xml_filenames)
    parse_upsert_xmls(xml_filenames, qb_stat_descs, stat_descs, stat_with_dash_descs, rare_stat_descs, rare_stat_with_dash_descs)

### DB close
conn.commit()
cur.close()
conn.close()
