import os
import re
import sys
import xml.dom.minidom as xml
from nfldb import standard_team
from stadium import standard_stadium

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

def print_xmls_as_csv(xml_filenames, qb_stat_descs, stat_descs, stat_with_dash_descs, rare_stat_descs, rare_stat_with_dash_descs):
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

        print_ary_as_csv_line(output)

qb_stat_descs = ['name', 'pass attempts', 'completions', 'pass yards', 'sacks', 'sack yardage', 'pass tds', 'long pass', 'interceptions', 'rating', 'rush attempts', 'rush yards', 'yards per rush', 'rush tds', 'long rush']
stat_descs = ['third downs converted', 'third downs', 'third down convert percent', 'fourth downs converted', 'fourth downs', 'fourth down convert percent', 'tackles for a loss', 'tackles for a loss yardage', 'times thrown', 'yards lost attempting to pass', 'pass attempts', 'completions', 'had intercepted', 'n kickoffs', 'n kickoffs in endzone', 'n kickoffs touchbacks', 'n punts', 'avg punt', 'fgs had blocked', 'pats had blocked', 'n punt returns', 'yards punt returns', 'n kickoff returns', 'yards kickoff returns', 'n interception returns', 'yards interception returns', 'n penalties', 'penalty yards', 'n fumbles', 'n fumbles lost', 'extra points made', 'extra points attempts', 'kicking made', 'kicking attempts', 'field goals made', 'field goals attempts', 'red zone converts', 'red zone attempts', 'red zone convert percentage', 'goal to go converts', 'goal to go attempts', 'goal to go convert percentage', 'time of possession', 'total first downs', 'by rushing', 'by passing', 'by penalty', 'total net yards', 'total offensive plays (inc. times thrown passing)', 'average gain per offensive play', 'net yards rushing', 'total rushing plays', 'average gain per rushing play', 'net yards passing', 'gross yards passing', 'avg gain per pass play (inc.# thrown passing)', 'had blocked', 'net punting average', 'total return yardage (not including kickoffs)', 'touchdowns', 'rushing', 'passing', 'safeties', 'final score']
stat_with_dash_descs = ['third down efficiency', 'fourth down efficiency', 'tackles for a loss-number and yards', 'times thrown - yards lost attempting to pass', 'pass attempts-completions-had intercepted', 'kickoffs number-in end zone-touchbacks', 'punts number and average', 'fgs - pats had blocked', 'no. and yards punt returns', 'no. and yards kickoff returns', 'no. and yards interception returns', 'penalties number and yards', 'fumbles number and lost', 'extra points made-attempts', 'kicking made-attempts', 'field goals made-attempts', 'red zone efficiency', 'goal to go efficiency']
rare_stat_descs = ['fumbles', 'interceptions', 'punt returns', 'kickoff returns', 'other (blocked kicks, etc.)']
rare_stat_with_dash_descs = ['rushing made-attempts', 'passing made-attempts']

# print csv header
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
print header

# get gamebook filenames in a sorted list
gamebooks_path = './gamebook-xml'
#xml_filenames = get_filenames(gamebooks_path, "2015-08-Reg-56621", ".xml")
years = range(2001, 2016)
for year in years:
    xml_filenames = get_filenames(gamebooks_path, str(year), ".xml")
    sort_nicely(xml_filenames)
    print_xmls_as_csv(xml_filenames, qb_stat_descs, stat_descs, stat_with_dash_descs, rare_stat_descs, rare_stat_with_dash_descs)

