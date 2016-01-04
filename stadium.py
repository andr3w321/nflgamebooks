import sys

stadiums = [
    ['3COM Park', '3COM', '3COM PARK', '3COM Park at Candlestick Park', '3Com', '3Com Park', '3ComPark', 'Monster Park', 'Candlestick Park', 'San Francisco Stadium @ Candlestick'],
    ['AT&T Stadium', 'AT&T', 'Cowboys', 'Cowboys Stadium'],
    ['Alamo Dome', 'Alamodome'],
    ['Arrowhead Stadium', 'Arrowhead', 'ARROWHEAD STADIUM', 'Arrowhead Stadiium'],
    ['Azteca Stadium'],
    ['Bank of America Stadium', 'Bank Of America Stadium', 'Bank of America', 'Bank of America Stadiium', 'Bank of America stadium', 'Ericsson', 'Ericcson Stadium', 'Ericsson Stadium', 'Erricsson Stadium'],
    ['CenturyLink Field', 'Qwest Field', 'Qwest Fieled', 'Qwest Stadium', 'Seahawks Stadium', 'CenturyLink', 'CenturyField'],
    ['Cinergy Field', 'Cinery Field, Cincinnati, OH', 'Cinergy', 'Bruce Coslett'],
    ['Dudley Field', 'Dudley Field - Vanderbilt Univ', 'Dudley Field-Vanderbilt Univ'],
    ['Edward Jones Dome', 'Edwards Jones Dome', "Dome at America\'s Center", 'Trans World Dome', 'Trans World'],
    ['EverBank Field', 'EverBank', 'Everbank Field', 'Jacksonville Municipal Stadium', 'Alltel Stadium', 'Alltel', 'Alltell', 'Alltell Stadium', 'ALLTEL Stadium', 'ALLTELL Stadium', 'alltel Stadium'],
    ['FedExField', 'FedEXField', 'FedEx', 'FedEx Field', 'Fedex Field', 'FedexField', 'Redskins Stadium', 'Redskins', 'Jack Kent Cooke Stadium'],
    ['FirstEnergy Stadium', 'First Energy Stadium', 'Cleveland Browns Stadium', 'Clevelan Browns Stadium', 'Cleveland', 'Cleveland  Browns Stadium', 'Cleveland Brown Stadium', 'Cleveland Browns', 'CLEVELAND BROWNS STADIUM', 'Cleveland Stadium'],
    ['Ford Field'],
    ['Foxboro Stadium', 'Foxboro'],
    ['Georgia Dome', 'GEORGIA DOME', 'Geogia Dome', 'George Dome', 'Georgia', 'The GEORGIA Dome', 'The Georgia Dome'],
    ['Gillette Stadium'],
    ['Heinz Field', 'Heinz Field (64,350)', 'Heniz Field'],
    ['Husky Stadium', 'Husky Staduim'],
    ['Kingdome', 'Kingdome, Seattle WA'],
    ['Lambeau Field', 'Lambeau', 'Lambeau Filed', 'Lambeau field'],
    ["Levi\'s Stadium", 'Levi Stadium'],
    ['Lincoln Financial Field', 'Lincoln Financal Field', 'Lincoln Financial FIeld','Lincoln Finacial Field'],
    ['Lucas Oil Stadium', 'Lucas Oil'],
    ['M&T Bank Stadium', 'M & T BANK STADIUM', 'M & T Bank', 'M & T Bank Satdium', 'M & T Bank Stadium', 'M&T Bank', 'M&T Stadium', 'New Stadium at Camden Yards', 'Ravens Stadium', 'PSINet Stadium', 'PSINET', 'PSINET Stadium', 'PSINet'],
    ['Memorial Stadium'],
    ['Mercedes-Benz Superdome', 'Mercedez-Benz Superdome', 'Louisiana Superdome'],
    ['MetLife Stadium', 'MetLife', 'MetLifeStadium', 'Metlife Stadium', 'The New Meadowlands Stadium', 'New Meadowlands Stadium'],
    ['Metrodome', 'Medtrodome', 'Metrodome Minneapolis', 'Minneapolis', 'Mall of America Field at HHH Metrodome', 'Mall of America Field at the HHH Metrodome', 'Mall of America Field, HHH Metrodome'],
    ['Sports Authority Field at Mile High', 'Sports Authority Field', 'Mile High Stadium', 'Mile High', 'Mile High Stadiumj', 'Mile High, Den Co', 'Invesco Field at Mile High', 'INVESCO Field at Mile High', 'Invesco Field at MIle High', 'Invesco at Mile High'],
    ['Mississippi Veterans Memorial Stadium'],
    ['NRG Stadium', 'NRG', 'NRG STADIUM', 'nrg Stadium', 'Reliant Stadium', 'Reliant'],
    ['Nissan Stadium', 'LP Field', 'Adelphia Coliseum', 'Adelphia', 'Adelphia Colisum', 'The Coliseum'],
    ['O.co Coliseum', 'O. Co', 'O. Co Coliseum', 'O. co Coliseum', 'O.Co Coliseum', 'O.Co Colisuem', 'O.Co Oakland Coliseum', 'O.co Coliseum Oakland', 'O.co Colisuem', 'McAfee Coliseum', 'Oakland-Alameda County Coliseum', 'Oakland - Alameda County Coliseum', 'Oakland -Alameda County Coliseum', 'Oakland -Alameda County Colisuem', 'Oakland -Alemeda County Coliseum', 'Oakland Alameda County Coliseum', 'Oakland Coliseum', 'Oakland-Alemeda County Coliseum', 'Network Associates Coliseum', 'Network  Associates Coliseum', 'Network Associates', 'Network Associates  Coliseum', 'Network Associates Coiseum', 'Network Associates Coliseuim', 'Network Associates Colisuem', 'Network Association Coliseum', 'Network Assoicates Coliseum', 'Networks Associates Coliseum, Oakland, CA USA'],
    ['Paul Brown Stadium'],
    ['Pontiac Silverdome', 'Pontiac', 'Pontiac Silverdome, Pontiac', 'Pontiac Sliverdome', 'Silverdome'],
    ['Qualcomm Stadium', 'Snapdragon Stadium'],
    ['RCA Dome', 'RCA', 'RCA DOME'],
    ['Ralph Wilson Stadium', 'Ralph Wilson', 'Rich Stadium', 'The Stadium', 'The Stadium, Orchard Park NY'],
    ['Raymond James Stadium', 'Raymond James', 'Raymond James STadium', 'Raymond James, Tampa, Florida'],
    ['Rogers Centre'],
    ['Ross-Ade Stadium'],
    ['Soldier Field', 'Soldier', 'Soldier Field, Chicago', 'Soldier field', 'Solider Field', 'soldier Field'],
    ['Sun Devil Stadium', 'Sun Devil', 'Sun Devil Staduim'],
    ['Sun Life Stadium', 'SunLife Stadium', 'Pro Player Stadium', 'Pro Player', 'Dolphin Stadium', 'Dolphins Stadium', 'Land Shark Stadium'],
    ['TCF Bank Stadium', 'TCF BANK STADIUM', 'TCF Bank Staduim'],
    ['Texas', 'Texas Stadium'],
    ['The Meadowlands', 'Meadowlands', 'Giants Stadium', 'Giants'],
    ['Three Rivers Stadium', 'Three Rivers', 'AT Three River Stadium'],
    ['Tiger Stadium'],
    ['Independence Stadium', 'Independence Bowl'],
    ['Tokyo Dome'],
    ['Tom Benson Hall of Fame Stadium', 'Fawcett Stadium', 'Hall of Fame Field at Fawcett Stadium', 'Pro Football Field at Fawcett Stadium'],
    ['University of Phoenix', 'Univeristy of Phoenix', 'Univerity of Phoenix Stadium', 'University Of Phoenix', 'University of Phoenix Stadium', 'University of Phoenix Staduim', 'University of Phoenix Statium', 'Unviversity of Phoenix Stadium', 'Cardinals Stadium', 'Cardinal Stadium'],
    ['Veterans Stadium', "Veteran\'s Stadium", 'Veterans'],
    ['Wembley Stadium', 'Wembley'],
    ['UNK']
]

def standard_stadium(stadium):
    lowercase_stadium = stadium.lower()
    for variants in stadiums:
        for variant in variants:
            if lowercase_stadium == variant.lower():
                return variants[0]
    sys.stderr.write("Unknown stadium {}".format(stadium))
    return stadium
