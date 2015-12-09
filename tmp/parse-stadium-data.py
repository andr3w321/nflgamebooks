import pandas as pd
df = pd.read_csv("output.csv")
pd.set_option('display.max_rows', len(df))
print df.groupby('stadium').size()
df[['year','home_team','stadium']]
df[['year','home_team','stadium']].drop_duplicates().sort(columns='home_team')
df2 = df[['home_team','stadium']].drop_duplicates().sort(columns='home_team')
teams = df2['home_team'].unique()
for team in teams:
    stadiums = {}
    stadiums[team] = df2[df2['home_team'] == team]['stadium'].values.tolist()
    #stadiums = df2[df2['home_team'] == team]['stadium'].values.tolist()
    print stadiums

'''
{'ARI': ['Sun Devil Stadium', 'Sun Devil', 'Sun Devil Staduim', 'Azteca Stadium', 'Cardinals Stadium', 'Cardinal Stadium', 'University of Phoenix Staduim', 'University of Phoenix Stadium', 'University of Phoenix', 'University Of Phoenix', 'Raymond James Stadium', 'Univeristy of Phoenix', 'University of Phoenix Statium', 'Unviversity of Phoenix Stadium', 'Univerity of Phoenix Stadium']}
{'ATL': ['Georgia Dome', 'Georgia', 'GEORGIA DOME', 'The Georgia Dome', nan, 'George Dome', 'The GEORGIA Dome', 'Geogia Dome', 'Wembley']}
{'BAL': ['New Stadium at Camden Yards', 'PSINET Stadium', 'PSINET', 'PSINet Stadium', 'PSINet', 'Ravens Stadium', 'M&T Bank Stadium', 'M & T BANK STADIUM', 'M & T Bank Stadium', 'M&T Bank', 'M & T Bank', 'M&T Stadium', 'M & T Bank Satdium']}
{'BUF': ['Ralph Wilson Stadium', 'The Stadium', 'The Stadium. Orchard Park NY', 'Rich Stadium', 'Ralph Wilson', 'Rogers Centre', 'Hall of Fame Field at Fawcett Stadium', 'Ford Field']}
{'CAR': ['Ericsson Stadium', 'Ericcson Stadium', 'Ericsson', 'Erricsson Stadium', 'Bank of America Stadium', 'Bank Of America Stadium', 'Bank of America stadium', 'Bank of America', 'Bank of America Stadiium']}
{'CHI': ['Soldier Field', 'Soldier', 'Soldier Field. Chicago', 'soldier Field', 'Memorial Stadium', 'Soldier field', 'Dolphin Stadium', 'Solider Field']}
{'CIN': ['Cinergy Field', 'Cinery Field. Cincinnati. OH', 'Bruce Coslett', 'Cinergy', 'Paul Brown Stadium', 'Fawcett Stadium']}
{'CLE': ['Cleveland  Browns Stadium', 'Cleveland Browns Stadium', 'Cleveland Browns', 'CLEVELAND BROWNS STADIUM', 'Cleveland', 'Cleveland Stadium', 'Cleveland Brown Stadium', 'Clevelan Browns Stadium', 'FirstEnergy Stadium', 'First Energy Stadium']}
{'DAL': ['Texas Stadium', 'Texas', 'Tokyo Dome', 'Azteca Stadium', 'Cowboys', 'Fawcett Stadium', 'AT&T Stadium', 'AT&T']}
{'DEN': ['Mile High Stadium', 'Mile High', 'Mile High. Den Co', 'Mile High Stadiumj', 'Invesco Field at Mile High', 'Invesco Field at MIle High', 'Invesco at Mile High', 'INVESCO Field at Mile High', 'Sports Authority Field at Mile High', 'MetLife Stadium', 'Sports Authority Field']}
{'DET': ['Pontiac Silverdome', 'Pontiac Silverdome. Pontiac', 'Pontiac', 'Silverdome', 'Pontiac Sliverdome', nan, 'Ford Field']}
{'GB': ['Lambeau Field', 'Lambeau', 'Lambeau field', 'Lambeau Filed', 'Cowboys Stadium']}
{'HOU': ['Reliant', 'Reliant Stadium', 'NRG Stadium', 'nrg Stadium', 'NRG STADIUM', 'NRG']}
{'IND': ['RCA Dome', 'RCA', 'Ross-Ade Stadium', 'RCA DOME', nan, 'Lucas Oil Stadium', 'Sun Life Stadium']}
{'JAC': ['Alltel Stadium', 'Alltell Stadium', 'Alltel', 'Alltell', 'ALLTEL Stadium', 'ALLTELL Stadium', 'alltel Stadium', 'Jacksonville Municipal Stadium', 'EverBank Field', 'Everbank Field', 'Wembley Stadium', 'EverBank']}
{'KC': ['Arrowhead Stadium', 'ARROWHEAD STADIUM', 'Arrowhead', 'Arrowhead Stadiium']}
{'MIA': ['Pro Player Stadium', 'Pro Player', nan, 'Dolphins Stadium', 'Dolphin Stadium', 'Wembley Stadium', 'Land Shark Stadium', 'Sun Life Stadium', 'SunLife Stadium']}
{'MIN': ['Metrodome', 'Metrodome Minneapolis', 'Minneapolis', 'Medtrodome', 'Mall of America Field at HHH Metrodome', 'Mall of America Field at the HHH Metrodome', 'Mall of America Field. HHH Metrodome', 'Ford Field', 'TCF Bank Stadium', 'Wembley Stadium', 'TCF Bank Staduim', 'TCF BANK STADIUM', 'Tom Benson Hall of Fame Stadium']}
{'NE': ['Foxboro Stadium', 'Foxboro', 'Louisiana Superdome', 'Gillette Stadium', 'Reliant Stadium', 'University of Phoenix Stadium', 'Lucas Oil Stadium']}
{'NO': ['Louisiana Superdome', 'Alamodome', 'Giants Stadium', 'Alamo Dome', 'Tiger Stadium', 'Independence Bowl', 'Mississippi Veterans Memorial Stadium', 'Wembley', 'Mercedes-Benz Superdome', 'Pro Football Field at Fawcett Stadium', 'Mercedez-Benz Superdome']}
{'NYG': ['Giants Stadium', 'Giants', 'Raymond James Stadium', 'New Meadowlands Stadium', 'MetLife Stadium', 'MetLifeStadium']}
{'NYJ': ['The Meadowlands', 'Meadowlands', 'Giants Stadium', 'The New Meadowlands Stadium', 'New Meadowlands Stadium', 'Metlife Stadium', 'MetLife Stadium', 'MetLife']}
{'OAK': ['Oakland Alameda County Coliseum', 'Network Associates Coliseum', 'Network Assoicates Coliseum', 'Networks Associates Coliseum. Oakland. CA USA', 'Network Associates', 'Network Association Coliseum', 'Network Associates  Coliseum', 'Network  Associates Coliseum', 'Network Associates Coiseum', 'Network Associates Colisuem', 'Network Associates Coliseuim', nan, 'McAfee Coliseum', 'Oakland-Alameda County Coliseum', 'Oakland - Alameda County Coliseum', 'Oakland -Alameda County Coliseum', 'Oakland -Alameda County Colisuem', 'Oakland -Alemeda County Coliseum', 'Oakland-Alemeda County Coliseum', 'O.co Coliseum', 'O. co Coliseum', 'O. Co', 'O.Co Colisuem', 'O.Co Coliseum', 'O.co Colisuem', 'Oakland Coliseum', 'O.Co Oakland Coliseum', 'O.co Coliseum Oakland', 'Wembley Stadium', 'O. Co Coliseum']}
{'PHI': ['Veterans Stadium', 'Veterans', "Veteran's Stadium", 'Lincoln Financial Field', 'ALLTEL Stadium', 'Lincoln Financial FIeld', 'Lincoln Financal Field']}
{'PIT': ['Three Rivers Stadium', 'AT Three River Stadium', 'Three Rivers', 'Azteca Stadium', 'Heinz Field', 'Heniz Field', 'Heinz Field (64.350)', 'Ford Field']}
{'SD': ['Qualcomm Stadium', nan, 'Sun Devil Stadium', 'Snapdragon Stadium']}
{'SEA': ['Kingdome', 'Kingdome. Seattle WA', 'Husky Stadium', nan, 'Husky Staduim', 'Seahawks Stadium', 'Qwest Field', 'Qwest Stadium', 'Qwest Fieled', 'CenturyLink Field', 'University of Phoenix']}
{'SF': ['3Com Park', '3Com', '3COM Park', '3ComPark', 'Candlestick Park', 'San Francisco Stadium @ Candlestick', '3COM Park at Candlestick Park', '3COM', 'Monster Park', '3COM PARK', 'Wembley Stadium', 'Mercedes-Benz Superdome', "Levi's Stadium", 'Levi Stadium']}
{'STL': ['Trans World Dome', 'Trans World', "Dome at America's Center", 'Edward Jones Dome', 'Edwards Jones Dome', 'Wembley Stadium']}
{'TB': ['Raymond James Stadium', 'Raymond James', 'Raymond James. Tampa. Florida', 'Qualcomm Stadium', 'Wembley Stadium', 'Raymond James STadium']}
{'TEN': ['Dudley Field', 'Dudley Field - Vanderbilt Univ', 'Dudley Field-Vanderbilt Univ', 'Adelphia', 'Adelphia Coliseum', 'Georgia', 'Adelphia Colisum', 'The Coliseum', 'LP Field', 'Fawcett Stadium', 'Nissan Stadium']}
{'WAS': ['Jack Kent Cooke Stadium', 'FedEx', 'Redskins Stadium', 'Redskins', 'FedEx Field', 'FedExField', nan, 'FedexField', 'FedEXField', 'Fedex Field']}

3COM                                               1
3COM PARK                                          1
3COM Park                                         35
3COM Park at Candlestick Park                      1
3Com                                               2
3Com Park                                         15
3ComPark                                           1
ALLTEL Stadium                                    41
ALLTELL Stadium                                    1
ARROWHEAD STADIUM                                  2
AT Three River Stadium                             1
AT&T                                               6
AT&T Stadium                                      20
Adelphia                                           1
Adelphia Coliseum                                 28
Adelphia Colisum                                   1
Alamo Dome                                         2
Alamodome                                          2
Alltel                                            12
Alltel Stadium                                    27
Alltell                                            2
Alltell Stadium                                    2
Arrowhead                                         16
Arrowhead Stadiium                                 1
Arrowhead Stadium                                151
Azteca Stadium                                     3
Bank Of America Stadium                            2
Bank of America                                    3
Bank of America Stadiium                           1
Bank of America Stadium                          110
Bank of America stadium                            1
Bruce Coslett                                      1
CLEVELAND BROWNS STADIUM                           1
Candlestick Park                                  63
Cardinal Stadium                                   1
Cardinals Stadium                                  4
CenturyLink Field                                 49
Cinergy                                            1
Cinergy Field                                     10
Cinery Field. Cincinnati. OH                       1
Clevelan Browns Stadium                            1
Cleveland                                          1
Cleveland  Browns Stadium                          1
Cleveland Brown Stadium                            2
Cleveland Browns                                   1
Cleveland Browns Stadium                         129
Cleveland Stadium                                  1
Cowboys                                           41
Cowboys Stadium                                    1
Dolphin Stadium                                   34
Dolphins Stadium                                   7
Dome at America's Center                          12
Dudley Field                                       4
Dudley Field - Vanderbilt Univ                     1
Dudley Field-Vanderbilt Univ                       1
Edward Jones Dome                                128
Edwards Jones Dome                                 6
Ericcson Stadium                                   1
Ericsson                                          36
Ericsson Stadium                                  16
Erricsson Stadium                                  1
EverBank                                           1
EverBank Field                                    46
Everbank Field                                     6
Fawcett Stadium                                    3
FedEXField                                         1
FedEx                                              2
FedEx Field                                        6
FedExField                                       146
Fedex Field                                        3
FedexField                                         2
First Energy Stadium                               1
FirstEnergy Stadium                               24
Ford Field                                       138
Foxboro                                            5
Foxboro Stadium                                   30
GEORGIA DOME                                       2
Geogia Dome                                        1
George Dome                                        1
Georgia                                            2
Georgia Dome                                     121
Giants                                             1
Giants Stadium                                   120
Gillette Stadium                                 150
Hall of Fame Field at Fawcett Stadium              1
Heinz Field                                      154
Heinz Field (64.350)                               1
Heniz Field                                        1
Husky Stadium                                     18
Husky Staduim                                      1
INVESCO Field at Mile High                         3
Independence Bowl                                  1
Invesco Field at MIle High                         1
Invesco Field at Mile High                        97
Invesco at Mile High                               1
Jack Kent Cooke Stadium                            6
Jacksonville Municipal Stadium                    30
Kingdome                                          13
Kingdome. Seattle WA                               1
LP Field                                          91
Lambeau                                            1
Lambeau Field                                    176
Lambeau Filed                                      2
Lambeau field                                      1
Land Shark Stadium                                10
Levi Stadium                                       1
Levi's Stadium                                    14
Lincoln Financal Field                             1
Lincoln Financial FIeld                            1
Lincoln Financial Field                          130
Louisiana Superdome                              119
Lucas Oil Stadium                                 81
M & T BANK STADIUM                                 1
M & T Bank                                         1
M & T Bank Satdium                                 1
M & T Bank Stadium                                27
M&T Bank                                           4
M&T Bank Stadium                                  80
M&T Stadium                                       14
Mall of America Field at HHH Metrodome            43
Mall of America Field at the HHH Metrodome         1
Mall of America Field. HHH Metrodome               1
McAfee Coliseum                                   33
Meadowlands                                       12
Medtrodome                                         1
Memorial Stadium                                  12
Mercedes-Benz Superdome                           41
Mercedez-Benz Superdome                            2
MetLife                                           17
MetLife Stadium                                   66
MetLifeStadium                                     1
Metlife Stadium                                    6
Metrodome                                        105
Metrodome Minneapolis                              3
Mile High                                          6
Mile High Stadium                                 16
Mile High Stadiumj                                 1
Mile High. Den Co                                  1
Minneapolis                                        1
Mississippi Veterans Memorial Stadium              1
Monster Park                                      36
NRG                                                1
NRG STADIUM                                        1
NRG Stadium                                       12
Network  Associates Coliseum                       1
Network Associates                                 1
Network Associates  Coliseum                       1
Network Associates Coiseum                         1
Network Associates Coliseuim                       1
Network Associates Coliseum                       54
Network Associates Colisuem                        1
Network Association Coliseum                       1
Network Assoicates Coliseum                        1
Networks Associates Coliseum. Oakland. CA USA      1
New Meadowlands Stadium                           14
New Stadium at Camden Yards                        6
Nissan Stadium                                     5
O. Co                                              1
O. Co Coliseum                                     1
O. co Coliseum                                     1
O.Co Coliseum                                      7
O.Co Colisuem                                      1
O.Co Oakland Coliseum                              1
O.co Coliseum                                     29
O.co Coliseum Oakland                              1
O.co Colisuem                                      1
Oakland - Alameda County Coliseum                  1
Oakland -Alameda County Coliseum                   1
Oakland -Alameda County Colisuem                   1
Oakland -Alemeda County Coliseum                   1
Oakland Alameda County Coliseum                    6
Oakland Coliseum                                   1
Oakland-Alameda County Coliseum                   18
Oakland-Alemeda County Coliseum                    1
PSINET                                             6
PSINET Stadium                                     2
PSINet                                             3
PSINet Stadium                                    18
Paul Brown Stadium                               158
Pontiac                                            1
Pontiac Silverdome                                27
Pontiac Silverdome. Pontiac                        2
Pontiac Sliverdome                                 1
Pro Football Field at Fawcett Stadium              1
Pro Player                                         4
Pro Player Stadium                                61
Qualcomm Stadium                                 172
Qwest Field                                       72
Qwest Fieled                                       1
Qwest Stadium                                      3
RCA                                                3
RCA DOME                                           1
RCA Dome                                          91
Ralph Wilson                                       2
Ralph Wilson Stadium                             154
Ravens Stadium                                    10
Raymond James                                      7
Raymond James STadium                              1
Raymond James Stadium                            164
Raymond James. Tampa. Florida                      1
Redskins                                           1
Redskins Stadium                                   3
Reliant                                           31
Reliant Stadium                                   92
Rich Stadium                                       1
Rogers Centre                                      8
Ross-Ade Stadium                                   1
San Francisco Stadium @ Candlestick                1
Seahawks Stadium                                  20
Silverdome                                         2
Snapdragon Stadium                                 1
Soldier                                            3
Soldier Field                                    153
Soldier Field. Chicago                             2
Soldier field                                      1
Solider Field                                      1
Sports Authority Field                             1
Sports Authority Field at Mile High               48
Sun Devil                                          4
Sun Devil Stadium                                 68
Sun Devil Staduim                                  1
Sun Life Stadium                                  52
SunLife Stadium                                    2
TCF BANK STADIUM                                   3
TCF Bank Stadium                                  11
TCF Bank Staduim                                   2
Texas                                             82
Texas Stadium                                     23
The Coliseum                                      41
The GEORGIA Dome                                   1
The Georgia Dome                                  40
The Meadowlands                                   99
The New Meadowlands Stadium                        8
The Stadium                                        2
The Stadium. Orchard Park NY                       1
Three Rivers                                       4
Three Rivers Stadium                              19
Tiger Stadium                                      4
Tokyo Dome                                         1
Tom Benson Hall of Fame Stadium                    1
Trans World                                        4
Trans World Dome                                  23
Univeristy of Phoenix                              4
Univerity of Phoenix Stadium                       1
University Of Phoenix                              3
University of Phoenix                             59
University of Phoenix Stadium                     25
University of Phoenix Staduim                      1
University of Phoenix Statium                      1
Unviversity of Phoenix Stadium                     1
Veteran's Stadium                                  1
Veterans                                           6
Veterans Stadium                                  39
Wembley                                            2
Wembley Stadium                                   10
alltel Stadium                                     1
nrg Stadium                                        1
soldier Field                                      1
'''


'3COM Park', '3COM', '3COM PARK', '3COM Park at Candlestick Park', '3Com', '3Com Park', '3ComPark', 'Monster Park'
'AT&T Stadium', 'AT&T'
'Alamo Dome', 'Alamodome'
'Arrowhead Stadium', 'Arrowhead', 'ARROWHEAD STADIUM', 'Arrowhead Stadiium'
'Azteca Stadium' # Mexico City
'Bank of America Stadium', 'Bank Of America Stadium', 'Bank of America', 'Bank of America Stadiium', 'Bank of America stadium', 'Ericsson', 'Ericcson Stadium', 'Ericsson Stadium', 'Erricsson Stadium'
'Bruce Coslett'
'Candlestick Park', 'San Francisco Stadium @ Candlestick'
'Cinergy Field', 'Cinery Field. Cincinnati. OH', 'Cinergy'
'Cowboys', 'Cowboys Stadium'
'Dudley Field', 'Dudley Field - Vanderbilt Univ', 'Dudley Field-Vanderbilt Univ'
'Edward Jones Dome', 'Edwards Jones Dome', "Dome at America\'s Center", 'Trans World Dome', 'Trans World'
'EverBank Field', 'EverBank', 'Everbank Field', 'Jacksonville Municipal Stadium', 'Alltel Stadium', 'Alltel', 'Alltell', 'Alltell Stadium', 'ALLTEL Stadium', 'ALLTELL Stadium', 'alltel Stadium'
'FedExField', 'FedEXField', 'FedEx', 'FedEx Field', 'Fedex Field', 'FedexField', 'Redskins Stadium', 'Redskins', 'Jack Kent Cooke Stadium'
'FirstEnergy Stadium', 'First Energy Stadium', 'Cleveland Browns Stadium', 'Clevelan Browns Stadium', 'Cleveland', 'Cleveland  Browns Stadium', 'Cleveland Brown Stadium', 'Cleveland Browns', 'CLEVELAND BROWNS STADIUM', 'Cleveland Stadium'
'Ford Field'
'Foxboro Stadium', 'Foxboro'
'Georgia Dome', 'GEORGIA DOME', 'Geogia Dome', 'George Dome', 'Georgia', 'The GEORGIA Dome', 'The Georgia Dome'
'Giants Stadium', 'Giants'
'Gillette Stadium'
'Heinz Field', 'Heinz Field (64.350)', 'Heniz Field'
'Husky Stadium', 'Husky Staduim'
'Invesco Field at Mile High', 'INVESCO Field at Mile High', 'Invesco Field at MIle High', 'Invesco at Mile High'
'Kingdome', 'Kingdome. Seattle WA'
'Lambeau Field', 'Lambeau', 'Lambeau Filed', 'Lambeau field'
"Levi\'s Stadium", 'Levi Stadium'
'Lincoln Financial Field', 'Lincoln Financal Field', 'Lincoln Financial FIeld'
'Lucas Oil Stadium'
'M&T Bank Stadium', 'M & T BANK STADIUM', 'M & T Bank', 'M & T Bank Satdium', 'M & T Bank Stadium', 'M&T Bank', 'M&T Stadium', 'New Stadium at Camden Yards', 'Ravens Stadium', 'PSINet Stadium', 'PSINET', 'PSINET Stadium', 'PSINet'
'Mall of America Field at HHH Metrodome', 'Mall of America Field at the HHH Metrodome', 'Mall of America Field. HHH Metrodome'
'Memorial Stadium'
'Mercedes-Benz Superdome', 'Mercedez-Benz Superdome', 'Louisiana Superdome'
'MetLife Stadium', 'MetLife', 'MetLifeStadium', 'Metlife Stadium'
'Metrodome', 'Medtrodome', 'Metrodome Minneapolis', 'Minneapolis'
'Sports Authority Field at Mile High', 'Sports Authority Field', 'Mile High Stadium', 'Mile High', 'Mile High Stadiumj', 'Mile High. Den Co'
'Mississippi Veterans Memorial Stadium'
'NRG Stadium', 'NRG', 'NRG STADIUM', 'nrg Stadium', 'Reliant Stadium', 'Reliant'
'Network Associates Coliseum', 'Network  Associates Coliseum', 'Network Associates', 'Network Associates  Coliseum', 'Network Associates Coiseum', 'Network Associates Coliseuim', 'Network Associates Colisuem', 'Network Association Coliseum', 'Network Assoicates Coliseum', 'Networks Associates Coliseum. Oakland. CA USA'
'Nissan Stadium', 'LP Field', 'Adelphia Coliseum', 'Adelphia', 'Adelphia Colisum', 'The Coliseum'
'O.co Coliseum', 'O. Co', 'O. Co Coliseum', 'O. co Coliseum', 'O.Co Coliseum', 'O.Co Colisuem', 'O.Co Oakland Coliseum', 'O.co Coliseum Oakland', 'O.co Colisuem', 'McAfee Coliseum', 'Oakland-Alameda County Coliseum', 'Oakland - Alameda County Coliseum', 'Oakland -Alameda County Coliseum', 'Oakland -Alameda County Colisuem', 'Oakland -Alemeda County Coliseum', 'Oakland Alameda County Coliseum', 'Oakland Coliseum', 'Oakland-Alemeda County Coliseum'
'Paul Brown Stadium'
'Pontiac Silverdome', 'Pontiac', 'Pontiac Silverdome. Pontiac', 'Pontiac Sliverdome', 'Silverdome'
'Qualcomm Stadium', 'Snapdragon Stadium'
'Qwest Field', 'Qwest Fieled', 'Qwest Stadium', 'Seahawks Stadium', 'CenturyLink Field'
'RCA Dome', 'RCA', 'RCA DOME'
'Ralph Wilson Stadium', 'Ralph Wilson', 'Rich Stadium'
'Raymond James Stadium', 'Raymond James', 'Raymond James STadium', 'Raymond James. Tampa. Florida'
'Rogers Centre' # Toronto, Ontario, Canada
'Ross-Ade Stadium'
'Soldier Field', 'Soldier', 'Soldier Field. Chicago', 'Soldier field', 'Solider Field', 'soldier Field'
'Sun Devil Stadium', 'Sun Devil', 'Sun Devil Staduim'
'Sun Life Stadium', 'SunLife Stadium', 'Pro Player Stadium', 'Pro Player', 'Dolphin Stadium', 'Dolphins Stadium', 'Land Shark Stadium'
'TCF Bank Stadium', 'TCF BANK STADIUM', 'TCF Bank Staduim'
'Texas', 'Texas Stadium'
'The Meadowlands', 'Meadowlands', 'The New Meadowlands Stadium', 'New Meadowlands Stadium'
'The Stadium', 'The Stadium. Orchard Park NY'
'Three Rivers Stadium', 'Three Rivers', 'AT Three River Stadium'
'Tiger Stadium'
'Independence Bowl'
'Tokyo Dome'
'Tom Benson Hall of Fame Stadium', 'Fawcett Stadium', 'Hall of Fame Field at Fawcett Stadium', 'Pro Football Field at Fawcett Stadium'
'University of Phoenix', 'Univeristy of Phoenix', 'Univerity of Phoenix Stadium', 'University Of Phoenix', 'University of Phoenix Stadium', 'University of Phoenix Staduim', 'University of Phoenix Statium', 'Unviversity of Phoenix Stadium', 'Cardinals Stadium', 'Cardinal Stadium'
'Veterans Stadium', "Veteran\'s Stadium", 'Veterans'
'Wembley Stadium', 'Wembley' # London, England
