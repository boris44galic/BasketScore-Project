import random
from datetime import date, datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Country, City, Hall, Season
from teams.models import Team
from leagues.models import League, LeagueTeam
from players.models import Player, Position, PlayerStats, PlayerMatchStatus
from matches.models import Match, Status


# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────

COUNTRIES = [
    "United States", "Canada", "Spain", "Germany", "Italy", "Greece",
    "Turkey", "France", "Lithuania", "Serbia", "Israel", "Monaco",
    "Australia", "Brazil", "Argentina", "Slovenia", "Croatia", "Bosnia and Herzegovina",
    "Montenegro", "North Macedonia", "Latvia", "Estonia", "Georgia",
    "Cameroon", "Nigeria", "Congo", "Egypt", "Senegal", "Sudan",
    "Dominican Republic", "Haiti", "Jamaica", "Trinidad and Tobago",
    "Russia", "Ukraine", "Czech Republic", "Hungary", "Poland",
]

# country -> list of (city, hall_name, hall_capacity)
CITIES_HALLS = {
    "United States": [
        ("Boston", "TD Garden", 19156),
        ("New York", "Madison Square Garden", 19812),
        ("Brooklyn", "Barclays Center", 17732),
        ("Philadelphia", "Wells Fargo Center", 20478),
        ("Chicago", "United Center", 20917),
        ("Cleveland", "Rocket Mortgage FieldHouse", 19432),
        ("Detroit", "Little Caesars Arena", 20491),
        ("Indianapolis", "Gainbridge Fieldhouse", 17923),
        ("Milwaukee", "Fiserv Forum", 17500),
        ("Atlanta", "State Farm Arena", 16600),
        ("Charlotte", "Spectrum Center", 19077),
        ("Miami", "Kaseya Center", 19600),
        ("Orlando", "Kia Center", 18846),
        ("Washington", "Capital One Arena", 20356),
        ("Denver", "Ball Arena", 19520),
        ("Minneapolis", "Target Center", 18978),
        ("Oklahoma City", "Paycom Center", 18203),
        ("Portland", "Moda Center", 19393),
        ("Salt Lake City", "Delta Center", 18306),
        ("San Francisco", "Chase Center", 18064),
        ("Los Angeles", "Crypto.com Arena", 18997),
        ("Inglewood", "Intuit Dome", 18000),
        ("Phoenix", "Footprint Center", 17125),
        ("Sacramento", "Golden 1 Center", 17500),
        ("Dallas", "American Airlines Center", 19200),
        ("Houston", "Toyota Center", 18055),
        ("Memphis", "FedExForum", 17794),
        ("New Orleans", "Smoothie King Center", 16867),
        ("San Antonio", "AT&T Center", 18418),
    ],
    "Canada": [
        ("Toronto", "Scotiabank Arena", 19800),
    ],
    "Spain": [
        ("Madrid", "WiZink Center", 17500),
        ("Barcelona", "Palau Blaugrana", 7585),
        ("Vitoria-Gasteiz", "Fernando Buesa Arena", 15504),
        ("Valencia", "Fuente de San Luis", 9000),
    ],
    "Germany": [
        ("Munich", "SAP Garden", 11500),
        ("Berlin", "Uber Arena", 14500),
    ],
    "Italy": [
        ("Milan", "Mediolanum Forum", 12700),
        ("Bologna", "Segafredo Arena", 5800),
    ],
    "Greece": [
        ("Athens", "OAKA Indoor Hall", 18400),
        ("Piraeus", "Peace and Friendship Stadium", 14500),
    ],
    "Turkey": [
        ("Istanbul", "Ulker Sports and Event Arena", 22000),
    ],
    "France": [
        ("Paris", "Adidas Arena", 8000),
    ],
    "Lithuania": [
        ("Kaunas", "Zalgirio Arena", 15426),
    ],
    "Serbia": [
        ("Belgrade", "Stark Arena", 22000),
    ],
    "Israel": [
        ("Tel Aviv", "Menora Mivtachim Arena", 11700),
    ],
    "Monaco": [
        ("Monaco", "Salle Gaston Médecin", 4480),
    ],
}

NBA_TEAMS = [
    # Atlantic
    ("Boston Celtics", "Boston", "United States"),
    ("New York Knicks", "New York", "United States"),
    ("Brooklyn Nets", "Brooklyn", "United States"),
    ("Philadelphia 76ers", "Philadelphia", "United States"),
    ("Toronto Raptors", "Toronto", "Canada"),
    # Central
    ("Chicago Bulls", "Chicago", "United States"),
    ("Cleveland Cavaliers", "Cleveland", "United States"),
    ("Detroit Pistons", "Detroit", "United States"),
    ("Indiana Pacers", "Indianapolis", "United States"),
    ("Milwaukee Bucks", "Milwaukee", "United States"),
    # Southeast
    ("Atlanta Hawks", "Atlanta", "United States"),
    ("Charlotte Hornets", "Charlotte", "United States"),
    ("Miami Heat", "Miami", "United States"),
    ("Orlando Magic", "Orlando", "United States"),
    ("Washington Wizards", "Washington", "United States"),
    # Northwest
    ("Denver Nuggets", "Denver", "United States"),
    ("Minnesota Timberwolves", "Minneapolis", "United States"),
    ("Oklahoma City Thunder", "Oklahoma City", "United States"),
    ("Portland Trail Blazers", "Portland", "United States"),
    ("Utah Jazz", "Salt Lake City", "United States"),
    # Pacific
    ("Golden State Warriors", "San Francisco", "United States"),
    ("Los Angeles Lakers", "Los Angeles", "United States"),
    ("LA Clippers", "Inglewood", "United States"),
    ("Phoenix Suns", "Phoenix", "United States"),
    ("Sacramento Kings", "Sacramento", "United States"),
    # Southwest
    ("Dallas Mavericks", "Dallas", "United States"),
    ("Houston Rockets", "Houston", "United States"),
    ("Memphis Grizzlies", "Memphis", "United States"),
    ("New Orleans Pelicans", "New Orleans", "United States"),
    ("San Antonio Spurs", "San Antonio", "United States"),
]

EUROLEAGUE_TEAMS = [
    ("Real Madrid", "Madrid", "Spain"),
    ("FC Barcelona", "Barcelona", "Spain"),
    ("EA7 Olimpia Milano", "Milan", "Italy"),
    ("Fenerbahce Beko", "Istanbul", "Turkey"),
    ("Anadolu Efes", "Istanbul", "Turkey"),
    ("Panathinaikos BC", "Athens", "Greece"),
    ("Olympiacos BC", "Piraeus", "Greece"),
    ("Bayern Munich Basketball", "Munich", "Germany"),
    ("Alba Berlin", "Berlin", "Germany"),
    ("Partizan Mozzart Bet", "Belgrade", "Serbia"),
    ("Crvena Zvezda", "Belgrade", "Serbia"),
    ("Maccabi Tel Aviv", "Tel Aviv", "Israel"),
    ("AS Monaco Basketball", "Monaco", "Monaco"),
    ("Saski Baskonia", "Vitoria-Gasteiz", "Spain"),
    ("Virtus Segafredo Bologna", "Bologna", "Italy"),
    ("Zalgiris Kaunas", "Kaunas", "Lithuania"),
    ("Valencia Basket", "Valencia", "Spain"),
    ("Paris Basketball", "Paris", "France"),
]

# team_name -> list of (first, last, country, position, dob, height_cm, weight_kg, wingspan_cm)
NBA_PLAYERS = {
    "Boston Celtics": [
        ("Jayson", "Tatum", "United States", "SF", "1998-03-03", 203, 95, 211),
        ("Jaylen", "Brown", "United States", "SG", "1996-10-24", 198, 101, 209),
        ("Kristaps", "Porzingis", "Latvia", "C", "1995-08-02", 221, 109, 224),
        ("Jrue", "Holiday", "United States", "PG", "1990-06-12", 193, 93, 203),
        ("Al", "Horford", "Dominican Republic", "C", "1986-06-03", 206, 109, 213),
        ("Derrick", "White", "United States", "SG", "1994-07-02", 193, 86, 198),
        ("Payton", "Pritchard", "United States", "PG", "1997-01-28", 185, 88, 191),
        ("Sam", "Hauser", "United States", "SF", "1997-12-08", 203, 97, 208),
        ("Luke", "Kornet", "United States", "C", "1995-07-15", 218, 111, 222),
        ("Xavier", "Tillman", "United States", "PF", "1999-01-12", 203, 106, 212),
    ],
    "New York Knicks": [
        ("Jalen", "Brunson", "United States", "PG", "1996-08-31", 185, 88, 193),
        ("Karl-Anthony", "Towns", "Dominican Republic", "C", "1995-11-15", 213, 109, 229),
        ("OG", "Anunoby", "Canada", "SF", "1997-07-17", 201, 99, 213),
        ("Josh", "Hart", "United States", "SG", "1995-03-06", 193, 100, 205),
        ("Mikal", "Bridges", "United States", "SG", "1996-08-30", 198, 95, 212),
        ("Julius", "Randle", "United States", "PF", "1994-11-29", 203, 113, 210),
        ("Precious", "Achiuwa", "Nigeria", "PF", "1999-09-19", 203, 104, 213),
        ("Miles", "McBride", "United States", "PG", "2000-09-08", 185, 86, 196),
        ("Isaiah", "Hartenstein", "Germany", "C", "1998-05-05", 213, 113, 221),
        ("Donte", "DiVincenzo", "United States", "SG", "1997-01-31", 193, 91, 203),
    ],
    "Brooklyn Nets": [
        ("Cam", "Thomas", "United States", "SG", "2002-10-05", 193, 89, 198),
        ("Ben", "Simmons", "Australia", "PG", "1996-07-20", 208, 105, 218),
        ("Cameron", "Johnson", "United States", "SF", "1996-03-03", 203, 97, 211),
        ("Dennis", "Schroder", "Germany", "PG", "1993-09-15", 185, 79, 193),
        ("Nic", "Claxton", "United States", "C", "1999-04-20", 211, 102, 218),
        ("Day'Ron", "Sharpe", "United States", "C", "2001-12-22", 211, 113, 218),
        ("Mikal", "Bridges", "United States", "SG", "1996-08-30", 198, 95, 212),
        ("Dorian", "Finney-Smith", "United States", "SF", "1993-05-04", 201, 99, 210),
        ("Spencer", "Dinwiddie", "United States", "PG", "1993-04-06", 196, 95, 203),
        ("Trendon", "Watford", "United States", "PF", "2001-02-22", 203, 104, 211),
    ],
    "Philadelphia 76ers": [
        ("Joel", "Embiid", "Cameroon", "C", "1994-03-16", 213, 127, 222),
        ("Paul", "George", "United States", "SF", "1990-05-02", 203, 100, 211),
        ("Tyrese", "Maxey", "United States", "PG", "2000-11-04", 185, 82, 193),
        ("Kelly", "Oubre Jr.", "United States", "SF", "1995-12-09", 198, 97, 208),
        ("Andre", "Drummond", "United States", "C", "1993-08-10", 208, 127, 218),
        ("Kyle", "Lowry", "United States", "PG", "1986-03-25", 180, 86, 187),
        ("Tobias", "Harris", "United States", "PF", "1992-07-15", 203, 104, 211),
        ("Marcus", "Morris Sr.", "United States", "PF", "1989-09-02", 203, 104, 211),
        ("Robert", "Covington", "United States", "SF", "1990-12-14", 201, 97, 211),
        ("Guerschon", "Yabusele", "France", "PF", "1995-12-17", 203, 108, 211),
    ],
    "Toronto Raptors": [
        ("Scottie", "Barnes", "United States", "SF", "2001-08-01", 206, 104, 218),
        ("RJ", "Barrett", "Canada", "SG", "2000-06-14", 198, 100, 206),
        ("Immanuel", "Quickley", "United States", "PG", "2000-06-17", 185, 84, 196),
        ("Jakob", "Poeltl", "Austria", "C", "1995-10-15", 213, 118, 220),
        ("Bruce", "Brown", "United States", "SG", "1996-08-15", 193, 97, 201),
        ("Precious", "Achiuwa", "Nigeria", "PF", "1999-09-19", 203, 104, 213),
        ("Gradey", "Dick", "United States", "SG", "2003-10-04", 196, 88, 204),
        ("Chris", "Boucher", "Canada", "PF", "1993-01-11", 206, 95, 216),
        ("Javon", "Freeman-Liberty", "United States", "SG", "1999-09-17", 193, 90, 200),
        ("Garrett", "Temple", "United States", "SG", "1986-05-08", 196, 97, 204),
    ],
    "Chicago Bulls": [
        ("Zach", "LaVine", "United States", "SG", "1995-03-10", 196, 91, 203),
        ("Nikola", "Vucevic", "Montenegro", "C", "1990-10-24", 211, 120, 218),
        ("Coby", "White", "United States", "PG", "2000-02-16", 191, 84, 198),
        ("Patrick", "Williams", "United States", "SF", "2001-08-26", 201, 99, 211),
        ("Andre", "Drummond", "United States", "C", "1993-08-10", 208, 127, 218),
        ("Alex", "Caruso", "United States", "PG", "1994-02-28", 191, 86, 200),
        ("Torrey", "Craig", "United States", "SF", "1990-12-08", 201, 99, 209),
        ("DeMar", "DeRozan", "United States", "SG", "1989-08-07", 198, 99, 203),
        ("Jevon", "Carter", "United States", "PG", "1995-09-16", 185, 88, 195),
        ("Dalen", "Terry", "United States", "SG", "2002-08-04", 196, 88, 206),
    ],
    "Cleveland Cavaliers": [
        ("Donovan", "Mitchell", "United States", "PG", "1996-09-07", 185, 98, 195),
        ("Darius", "Garland", "United States", "PG", "2000-01-26", 185, 84, 193),
        ("Evan", "Mobley", "United States", "C", "2001-06-18", 213, 104, 225),
        ("Jarrett", "Allen", "United States", "C", "1998-04-21", 211, 109, 218),
        ("Max", "Strus", "United States", "SG", "1996-03-28", 196, 97, 204),
        ("Caris", "LeVert", "United States", "SG", "1994-02-25", 196, 90, 204),
        ("Georges", "Niang", "United States", "PF", "1993-06-17", 203, 108, 210),
        ("Dean", "Wade", "United States", "SF", "1996-03-28", 203, 99, 211),
        ("Isaac", "Okoro", "United States", "SF", "2000-12-26", 196, 97, 207),
        ("Sam", "Merrill", "United States", "SG", "1997-11-20", 196, 95, 202),
    ],
    "Detroit Pistons": [
        ("Cade", "Cunningham", "United States", "PG", "2001-09-25", 201, 100, 209),
        ("Jalen", "Duren", "United States", "C", "2003-11-18", 213, 120, 220),
        ("Isaiah", "Stewart", "United States", "PF", "2001-05-22", 206, 113, 215),
        ("Bojan", "Bogdanovic", "Croatia", "SF", "1989-04-18", 203, 102, 209),
        ("Monte", "Morris", "United States", "PG", "1995-06-27", 188, 86, 197),
        ("Killian", "Hayes", "France", "PG", "2001-07-27", 193, 90, 200),
        ("Alec", "Burks", "United States", "SG", "1991-07-20", 196, 97, 204),
        ("Simone", "Fontecchio", "Italy", "SF", "1995-06-28", 201, 97, 209),
        ("James", "Wiseman", "United States", "C", "2001-03-31", 216, 113, 224),
        ("Malik", "Beasley", "United States", "SG", "1996-11-26", 193, 86, 200),
    ],
    "Indiana Pacers": [
        ("Tyrese", "Haliburton", "United States", "PG", "2000-02-29", 196, 84, 207),
        ("Pascal", "Siakam", "Cameroon", "PF", "1994-04-02", 206, 104, 213),
        ("Myles", "Turner", "United States", "C", "1996-03-24", 211, 113, 220),
        ("Bennedict", "Mathurin", "Canada", "SG", "2002-06-19", 196, 99, 204),
        ("Aaron", "Nesmith", "United States", "SF", "1999-10-16", 198, 97, 207),
        ("Obi", "Toppin", "United States", "PF", "1998-03-04", 206, 104, 213),
        ("Isaiah", "Jackson", "United States", "C", "2001-12-09", 211, 104, 220),
        ("Andrew", "Nembhard", "Canada", "PG", "2001-01-16", 193, 86, 200),
        ("T.J.", "McConnell", "United States", "PG", "1992-03-25", 185, 79, 193),
        ("Doug", "McDermott", "United States", "SF", "1991-01-03", 203, 104, 209),
    ],
    "Milwaukee Bucks": [
        ("Giannis", "Antetokounmpo", "Greece", "PF", "1994-12-06", 211, 109, 227),
        ("Damian", "Lillard", "United States", "PG", "1990-07-15", 185, 88, 193),
        ("Khris", "Middleton", "United States", "SF", "1991-08-12", 203, 102, 210),
        ("Brook", "Lopez", "United States", "C", "1988-04-01", 216, 122, 221),
        ("Malik", "Beasley", "United States", "SG", "1996-11-26", 193, 86, 200),
        ("Bobby", "Portis", "United States", "PF", "1995-02-10", 208, 111, 214),
        ("Pat", "Connaughton", "United States", "SG", "1993-01-06", 196, 97, 202),
        ("MarJon", "Beauchamp", "United States", "SF", "2001-07-24", 198, 95, 208),
        ("AJ", "Green", "United States", "SG", "1999-01-04", 196, 93, 202),
        ("Chris", "Livingston", "United States", "SF", "2003-07-10", 201, 97, 210),
    ],
    "Atlanta Hawks": [
        ("Trae", "Young", "United States", "PG", "1998-09-19", 185, 74, 193),
        ("Jalen", "Johnson", "United States", "PF", "2001-09-20", 206, 104, 218),
        ("Clint", "Capela", "Switzerland", "C", "1994-05-18", 208, 113, 220),
        ("Bogdan", "Bogdanovic", "Serbia", "SG", "1992-08-18", 196, 95, 204),
        ("Saddiq", "Bey", "United States", "SF", "1999-03-15", 201, 97, 210),
        ("Onyeka", "Okongwu", "United States", "C", "2001-04-12", 206, 104, 216),
        ("Garrison", "Mathews", "United States", "SG", "1996-10-24", 196, 95, 203),
        ("David", "Roddy", "United States", "SF", "2001-05-09", 201, 102, 209),
        ("Seth", "Lundy", "United States", "SG", "2001-05-09", 196, 91, 203),
        ("Kobe", "Bufkin", "United States", "SG", "2003-01-06", 193, 86, 200),
    ],
    "Charlotte Hornets": [
        ("LaMelo", "Ball", "United States", "PG", "2001-08-22", 201, 88, 211),
        ("Brandon", "Miller", "United States", "SF", "2003-05-22", 203, 95, 213),
        ("Miles", "Bridges", "United States", "PF", "1998-03-21", 201, 104, 210),
        ("Mark", "Williams", "United States", "C", "2001-10-28", 216, 113, 224),
        ("Terry", "Rozier", "United States", "PG", "1994-03-17", 185, 84, 196),
        ("Cody", "Martin", "United States", "SF", "1995-10-17", 198, 99, 207),
        ("Grant", "Williams", "United States", "PF", "1998-11-30", 201, 110, 209),
        ("Josh", "Green", "Australia", "SG", "2001-11-16", 198, 95, 207),
        ("Nick", "Smith Jr.", "United States", "PG", "2004-06-06", 193, 84, 200),
        ("Tre", "Mann", "United States", "PG", "2000-10-18", 191, 86, 199),
    ],
    "Miami Heat": [
        ("Jimmy", "Butler", "United States", "SF", "1989-09-14", 201, 104, 209),
        ("Bam", "Adebayo", "United States", "C", "1997-07-18", 206, 115, 213),
        ("Tyler", "Herro", "United States", "SG", "2000-01-20", 193, 91, 201),
        ("Terry", "Rozier", "United States", "PG", "1994-03-17", 185, 84, 196),
        ("Duncan", "Robinson", "United States", "SG", "1994-04-22", 203, 99, 208),
        ("Kyle", "Lowry", "United States", "PG", "1986-03-25", 180, 86, 187),
        ("Caleb", "Martin", "United States", "SF", "1995-09-28", 198, 97, 206),
        ("Nikola", "Jovic", "Serbia", "PF", "2003-06-07", 208, 102, 215),
        ("Josh", "Richardson", "United States", "SG", "1993-09-15", 196, 97, 205),
        ("Kevin", "Love", "United States", "PF", "1988-09-07", 208, 113, 213),
    ],
    "Orlando Magic": [
        ("Paolo", "Banchero", "United States", "PF", "2002-11-12", 208, 113, 218),
        ("Franz", "Wagner", "Germany", "SF", "2001-08-27", 206, 104, 213),
        ("Wendell", "Carter Jr.", "United States", "C", "1999-04-16", 208, 116, 217),
        ("Jalen", "Suggs", "United States", "PG", "2001-12-03", 193, 97, 204),
        ("Cole", "Anthony", "United States", "PG", "2001-05-13", 185, 86, 196),
        ("Moritz", "Wagner", "Germany", "C", "1997-04-26", 211, 109, 218),
        ("Markelle", "Fultz", "United States", "PG", "1998-05-29", 191, 95, 199),
        ("Jonathan", "Isaac", "United States", "PF", "1997-10-13", 211, 102, 220),
        ("Kentavious", "Caldwell-Pope", "United States", "SG", "1993-02-18", 196, 99, 203),
        ("Anthony", "Black", "United States", "PG", "2003-08-31", 201, 95, 210),
    ],
    "Washington Wizards": [
        ("Kyle", "Kuzma", "United States", "PF", "1995-07-24", 206, 104, 213),
        ("Jordan", "Poole", "United States", "SG", "2000-06-19", 193, 88, 200),
        ("Bilal", "Coulibaly", "France", "SF", "2004-01-05", 201, 91, 210),
        ("Alexandre", "Sarr", "France", "C", "2005-01-09", 216, 104, 224),
        ("Tyus", "Jones", "United States", "PG", "1996-05-10", 183, 75, 190),
        ("Richaun", "Holmes", "United States", "C", "1993-10-14", 208, 113, 214),
        ("Landry", "Shamet", "United States", "SG", "1997-03-13", 193, 84, 200),
        ("Corey", "Kispert", "United States", "SF", "1999-03-03", 203, 99, 210),
        ("Johnny", "Davis", "United States", "SG", "2003-01-19", 196, 97, 204),
        ("Justin", "Champagnie", "United States", "SF", "2001-10-18", 201, 95, 210),
    ],
    "Denver Nuggets": [
        ("Nikola", "Jokic", "Serbia", "C", "1995-02-19", 211, 129, 212),
        ("Jamal", "Murray", "Canada", "PG", "1997-02-23", 193, 97, 200),
        ("Michael", "Porter Jr.", "United States", "SF", "1998-06-29", 208, 104, 216),
        ("Aaron", "Gordon", "United States", "PF", "1995-09-16", 203, 108, 212),
        ("Kentavious", "Caldwell-Pope", "United States", "SG", "1993-02-18", 196, 99, 203),
        ("Reggie", "Jackson", "United States", "PG", "1990-04-16", 188, 88, 198),
        ("Peyton", "Watson", "United States", "SF", "2003-07-09", 206, 95, 216),
        ("Zeke", "Nnaji", "United States", "PF", "2000-08-14", 208, 109, 215),
        ("Christian", "Braun", "United States", "SG", "2002-11-29", 198, 97, 207),
        ("Julian", "Strawther", "United States", "SG", "2002-03-20", 198, 97, 206),
    ],
    "Minnesota Timberwolves": [
        ("Anthony", "Edwards", "United States", "SG", "2001-08-05", 193, 102, 204),
        ("Rudy", "Gobert", "France", "C", "1992-06-26", 216, 118, 234),
        ("Mike", "Conley", "United States", "PG", "1987-10-11", 183, 77, 193),
        ("Jaden", "McDaniels", "United States", "SF", "2001-06-13", 206, 95, 216),
        ("Naz", "Reid", "United States", "C", "1999-09-29", 208, 116, 215),
        ("Monte", "Morris", "United States", "PG", "1995-06-27", 188, 86, 197),
        ("Nickeil", "Alexander-Walker", "Canada", "SG", "1998-09-02", 196, 90, 204),
        ("Kyle", "Anderson", "United States", "SF", "1993-09-20", 208, 111, 220),
        ("Josh", "Minott", "Trinidad and Tobago", "SF", "2003-06-26", 201, 93, 210),
        ("Daishen", "Nix", "United States", "PG", "2002-02-03", 193, 93, 202),
    ],
    "Oklahoma City Thunder": [
        ("Shai", "Gilgeous-Alexander", "Canada", "PG", "2000-07-12", 198, 88, 208),
        ("Jalen", "Williams", "United States", "SG", "2001-07-04", 196, 97, 205),
        ("Chet", "Holmgren", "United States", "C", "2002-05-01", 213, 93, 225),
        ("Luguentz", "Dort", "Canada", "SG", "1999-04-19", 193, 97, 200),
        ("Josh", "Giddey", "Australia", "PG", "2002-10-10", 206, 99, 215),
        ("Isaiah", "Joe", "United States", "SG", "2000-06-17", 196, 88, 203),
        ("Kenrich", "Williams", "United States", "SF", "1994-12-04", 201, 99, 210),
        ("Aaron", "Wiggins", "United States", "SG", "2000-12-01", 196, 93, 204),
        ("Ousmane", "Dieng", "France", "SF", "2003-01-16", 208, 95, 215),
        ("Jaylin", "Williams", "United States", "PF", "2002-08-14", 206, 109, 215),
    ],
    "Portland Trail Blazers": [
        ("Anfernee", "Simons", "United States", "PG", "2000-01-08", 188, 79, 198),
        ("Jerami", "Grant", "United States", "SF", "1994-03-12", 201, 104, 210),
        ("Scoot", "Henderson", "United States", "PG", "2004-02-03", 188, 84, 198),
        ("Deandre", "Ayton", "Bahamas", "C", "1998-07-23", 213, 113, 220),
        ("Robert", "Williams III", "United States", "C", "1997-10-17", 208, 104, 218),
        ("Toumani", "Camara", "France", "SF", "2001-09-21", 203, 97, 212),
        ("Jabari", "Walker", "United States", "PF", "2002-09-23", 203, 104, 212),
        ("Matisse", "Thybulle", "United States", "SG", "1997-03-04", 198, 91, 207),
        ("Shaedon", "Sharpe", "Canada", "SG", "2003-05-25", 196, 93, 204),
        ("Malcolm", "Brogdon", "United States", "PG", "1992-12-11", 196, 102, 205),
    ],
    "Utah Jazz": [
        ("Lauri", "Markkanen", "Finland", "PF", "1997-05-22", 213, 109, 220),
        ("Jordan", "Clarkson", "United States", "SG", "1992-06-07", 191, 93, 199),
        ("Collin", "Sexton", "United States", "PG", "1999-01-04", 183, 84, 192),
        ("Walker", "Kessler", "United States", "C", "2001-08-26", 216, 108, 228),
        ("John", "Collins", "United States", "PF", "1997-09-23", 208, 108, 214),
        ("Keyonte", "George", "United States", "PG", "2003-12-30", 191, 82, 199),
        ("Talen", "Horton-Tucker", "United States", "SG", "2000-11-25", 198, 102, 207),
        ("Ochai", "Agbaji", "United States", "SG", "1999-12-18", 196, 95, 204),
        ("Brice", "Sensabaugh", "United States", "SF", "2003-04-22", 198, 104, 207),
        ("Kelly", "Olynyk", "Canada", "C", "1991-04-19", 213, 113, 218),
    ],
    "Golden State Warriors": [
        ("Stephen", "Curry", "United States", "PG", "1988-03-14", 188, 84, 196),
        ("Draymond", "Green", "United States", "PF", "1990-03-04", 198, 104, 207),
        ("Andrew", "Wiggins", "Canada", "SF", "1995-02-23", 201, 97, 210),
        ("Jonathan", "Kuminga", "Congo", "SF", "2002-10-06", 201, 104, 210),
        ("Moses", "Moody", "United States", "SG", "2002-05-31", 196, 95, 204),
        ("Brandin", "Podziemski", "United States", "SG", "2002-09-22", 193, 88, 200),
        ("Gary", "Payton II", "United States", "PG", "1992-12-01", 185, 90, 196),
        ("Trayce", "Jackson-Davis", "United States", "C", "2001-02-22", 208, 113, 217),
        ("Kevon", "Looney", "United States", "C", "1996-02-06", 208, 113, 215),
        ("Chris", "Paul", "United States", "PG", "1985-05-06", 183, 79, 191),
    ],
    "Los Angeles Lakers": [
        ("LeBron", "James", "United States", "SF", "1984-12-30", 206, 113, 213),
        ("Anthony", "Davis", "United States", "C", "1993-03-11", 208, 115, 220),
        ("D'Angelo", "Russell", "United States", "PG", "1996-02-23", 191, 84, 199),
        ("Austin", "Reaves", "United States", "SG", "1998-05-27", 196, 88, 204),
        ("Rui", "Hachimura", "Japan", "SF", "1998-02-08", 203, 102, 210),
        ("Gabe", "Vincent", "United States", "PG", "1996-06-14", 191, 88, 200),
        ("Jaxson", "Hayes", "United States", "C", "2000-06-05", 213, 107, 220),
        ("Taurean", "Prince", "United States", "SF", "1993-07-02", 201, 99, 208),
        ("Christian", "Wood", "United States", "C", "1995-09-27", 211, 104, 218),
        ("Spencer", "Dinwiddie", "United States", "PG", "1993-04-06", 196, 95, 203),
    ],
    "LA Clippers": [
        ("Kawhi", "Leonard", "United States", "SF", "1991-06-29", 201, 104, 213),
        ("James", "Harden", "United States", "SG", "1989-08-26", 196, 99, 206),
        ("Paul", "George", "United States", "SF", "1990-05-02", 203, 100, 211),
        ("Norman", "Powell", "United States", "SG", "1993-05-25", 193, 97, 201),
        ("Ivica", "Zubac", "Croatia", "C", "1997-03-18", 216, 120, 222),
        ("Terance", "Mann", "United States", "SF", "1997-12-18", 196, 102, 205),
        ("Mason", "Plumlee", "United States", "C", "1989-03-05", 211, 111, 218),
        ("Russell", "Westbrook", "United States", "PG", "1988-11-12", 191, 95, 200),
        ("Kris", "Dunn", "United States", "PG", "1994-08-18", 193, 93, 202),
        ("Brandon", "Boston Jr.", "United States", "SG", "2001-08-10", 196, 88, 205),
    ],
    "Phoenix Suns": [
        ("Kevin", "Durant", "United States", "SF", "1988-09-29", 208, 109, 218),
        ("Devin", "Booker", "United States", "SG", "1996-10-30", 196, 97, 204),
        ("Bradley", "Beal", "United States", "SG", "1993-06-28", 193, 97, 201),
        ("Jusuf", "Nurkic", "Bosnia and Herzegovina", "C", "1994-08-23", 213, 127, 218),
        ("Grayson", "Allen", "United States", "SG", "1995-10-08", 196, 97, 204),
        ("Eric", "Gordon", "United States", "SG", "1988-12-25", 193, 99, 200),
        ("Josh", "Okogie", "Nigeria", "SF", "1998-06-01", 193, 99, 204),
        ("Drew", "Eubanks", "United States", "C", "1996-06-14", 208, 111, 215),
        ("Royce", "O'Neale", "United States", "SF", "1993-06-05", 201, 104, 210),
        ("Ryan", "Dunn", "United States", "SG", "2004-01-07", 196, 93, 206),
    ],
    "Sacramento Kings": [
        ("De'Aaron", "Fox", "United States", "PG", "1997-12-20", 191, 83, 200),
        ("Domantas", "Sabonis", "Lithuania", "C", "1996-05-03", 211, 118, 214),
        ("Kevin", "Huerter", "United States", "SG", "1998-09-10", 201, 95, 209),
        ("Harrison", "Barnes", "United States", "SF", "1992-05-30", 203, 102, 210),
        ("Malik", "Monk", "United States", "PG", "1998-02-04", 188, 84, 197),
        ("Alex", "Len", "Ukraine", "C", "1993-06-16", 213, 118, 218),
        ("Trey", "Lyles", "United States", "PF", "1995-11-05", 208, 113, 215),
        ("Keon", "Ellis", "United States", "SG", "1999-03-21", 196, 86, 204),
        ("Colby", "Jones", "United States", "SF", "2002-09-18", 198, 93, 207),
        ("Jordan", "McLaughlin", "United States", "PG", "1997-02-06", 180, 77, 188),
    ],
    "Dallas Mavericks": [
        ("Luka", "Doncic", "Slovenia", "PG", "1999-02-28", 201, 104, 209),
        ("Kyrie", "Irving", "United States", "PG", "1992-03-23", 191, 88, 200),
        ("Derrick", "Jones Jr.", "United States", "SF", "1997-02-15", 198, 97, 208),
        ("PJ", "Washington", "United States", "PF", "1998-08-23", 203, 104, 212),
        ("Daniel", "Gafford", "United States", "C", "1998-10-01", 211, 107, 218),
        ("Josh", "Green", "Australia", "SG", "2001-11-16", 198, 95, 207),
        ("Maxi", "Kleber", "Germany", "PF", "1992-01-29", 211, 108, 216),
        ("Dante", "Exum", "Australia", "PG", "1995-07-13", 193, 88, 202),
        ("Richaun", "Holmes", "United States", "C", "1993-10-14", 208, 113, 214),
        ("Tim", "Hardaway Jr.", "United States", "SG", "1992-03-16", 196, 97, 204),
    ],
    "Houston Rockets": [
        ("Alperen", "Sengun", "Turkey", "C", "2002-07-25", 208, 113, 214),
        ("Jalen", "Green", "United States", "SG", "2002-02-09", 193, 86, 200),
        ("Fred", "VanVleet", "United States", "PG", "1994-02-25", 185, 86, 193),
        ("Amen", "Thompson", "United States", "SF", "2003-01-29", 201, 97, 211),
        ("Jabari", "Smith Jr.", "United States", "PF", "2003-10-09", 211, 104, 218),
        ("Dillon", "Brooks", "Canada", "SG", "1996-01-22", 196, 97, 204),
        ("Tari", "Eason", "United States", "SF", "2002-09-07", 203, 102, 212),
        ("Cam", "Whitmore", "United States", "SF", "2004-01-06", 201, 104, 210),
        ("Jeff", "Green", "United States", "PF", "1986-08-28", 206, 108, 213),
        ("Steven", "Adams", "New Zealand", "C", "1993-07-20", 213, 120, 220),
    ],
    "Memphis Grizzlies": [
        ("Ja", "Morant", "United States", "PG", "1999-08-10", 188, 79, 198),
        ("Jaren", "Jackson Jr.", "United States", "C", "1999-09-15", 211, 107, 218),
        ("Desmond", "Bane", "United States", "SG", "1998-06-25", 196, 97, 205),
        ("Marcus", "Smart", "United States", "PG", "1994-03-06", 188, 99, 197),
        ("Ziaire", "Williams", "United States", "SF", "2002-04-01", 201, 88, 210),
        ("Luke", "Kennard", "United States", "SG", "1996-06-20", 196, 95, 203),
        ("Bismack", "Biyombo", "Congo", "C", "1992-08-28", 208, 116, 214),
        ("John", "Konchar", "United States", "SG", "1996-03-31", 196, 97, 204),
        ("GG", "Jackson II", "United States", "PF", "2004-11-06", 206, 99, 213),
        ("Kenneth", "Lofton Jr.", "United States", "C", "2002-08-25", 206, 113, 213),
    ],
    "New Orleans Pelicans": [
        ("Zion", "Williamson", "United States", "PF", "2000-07-06", 198, 129, 208),
        ("Brandon", "Ingram", "United States", "SF", "1997-09-14", 206, 88, 213),
        ("CJ", "McCollum", "United States", "SG", "1991-09-19", 191, 86, 199),
        ("Herb", "Jones", "United States", "SF", "1998-04-01", 201, 95, 210),
        ("Jonas", "Valanciunas", "Lithuania", "C", "1992-05-06", 213, 120, 218),
        ("Trey", "Murphy III", "United States", "SF", "2001-06-07", 203, 95, 211),
        ("Jose", "Alvarado", "United States", "PG", "1998-08-13", 180, 77, 188),
        ("Larry", "Nance Jr.", "United States", "PF", "1993-01-01", 203, 106, 211),
        ("Dyson", "Daniels", "Australia", "SG", "2003-03-17", 198, 88, 208),
        ("Jordan", "Hawkins", "United States", "SG", "2002-08-08", 196, 88, 204),
    ],
    "San Antonio Spurs": [
        ("Victor", "Wembanyama", "France", "C", "2004-01-04", 224, 95, 240),
        ("Devin", "Vassell", "United States", "SG", "2000-08-23", 196, 91, 205),
        ("Jeremy", "Sochan", "United States", "PF", "2003-05-20", 206, 106, 215),
        ("Keldon", "Johnson", "United States", "SF", "2000-10-26", 198, 102, 207),
        ("Chris", "Paul", "United States", "PG", "1985-05-06", 183, 79, 191),
        ("Zach", "Collins", "United States", "C", "1997-11-18", 213, 111, 218),
        ("Julian", "Champagnie", "United States", "SF", "2001-10-18", 201, 95, 210),
        ("Tre", "Jones", "United States", "PG", "1999-01-26", 185, 82, 194),
        ("Charles", "Bassey", "Nigeria", "C", "2000-09-11", 211, 108, 218),
        ("Blake", "Wesley", "United States", "PG", "2003-03-10", 193, 84, 201),
    ],
}

EUROLEAGUE_PLAYERS = {
    "Real Madrid": [
        ("Sergio", "Llull", "Spain", "PG", "1987-11-15", 190, 90, 198),
        ("Facundo", "Campazzo", "Argentina", "PG", "1991-03-23", 179, 77, 188),
        ("Mario", "Hezonja", "Croatia", "SF", "1995-02-25", 203, 99, 211),
        ("Walter", "Tavares", "Cape Verde", "C", "1992-05-17", 221, 115, 227),
        ("Dzanan", "Musa", "Bosnia and Herzegovina", "SF", "1999-09-09", 203, 97, 211),
        ("Guerschon", "Yabusele", "France", "PF", "1995-12-17", 203, 108, 211),
        ("Alberto", "Abalde", "Spain", "SG", "1994-04-01", 198, 97, 206),
        ("Gabriel", "Deck", "Argentina", "PF", "1995-02-08", 203, 104, 211),
        ("Chus", "Mathews", "Spain", "PG", "1989-05-12", 188, 85, 196),
        ("Carlos", "Alocen", "Spain", "PG", "2000-12-17", 188, 82, 196),
    ],
    "FC Barcelona": [
        ("Nicolas", "Laprovittola", "Argentina", "PG", "1991-04-14", 180, 77, 188),
        ("Jan", "Vesely", "Czech Republic", "C", "1990-04-24", 213, 102, 220),
        ("Darius", "Thompson", "United States", "PG", "1994-01-12", 193, 84, 201),
        ("Jabari", "Parker", "United States", "PF", "1995-03-15", 203, 106, 211),
        ("Willy", "Hernangomez", "Spain", "C", "1994-05-27", 213, 107, 218),
        ("Rokas", "Jokubaitis", "Lithuania", "PG", "2001-10-10", 190, 84, 199),
        ("Joel", "Parra", "Spain", "SF", "2001-10-07", 201, 97, 210),
        ("Tomas", "Satoransky", "Czech Republic", "PG", "1991-10-30", 201, 97, 210),
        ("Ante", "Tomic", "Croatia", "C", "1988-06-18", 213, 118, 218),
        ("Darío", "Brizuela", "Spain", "SG", "1996-09-04", 193, 90, 201),
    ],
    "EA7 Olimpia Milano": [
        ("Shabazz", "Napier", "United States", "PG", "1991-07-14", 188, 84, 197),
        ("Nikola", "Mirotic", "Montenegro", "PF", "1991-02-07", 208, 109, 215),
        ("Shavon", "Shields", "United States", "SF", "1994-11-17", 201, 99, 210),
        ("Devon", "Hall", "United States", "SG", "1996-04-14", 196, 95, 204),
        ("Zach", "LeDay", "United States", "PF", "1994-08-15", 201, 104, 210),
        ("Diego", "Flaccadori", "Italy", "PG", "1997-09-19", 193, 86, 201),
        ("Stefano", "Tonut", "Italy", "SG", "1996-01-26", 196, 93, 204),
        ("Johannes", "Voigtmann", "Germany", "C", "1992-08-04", 213, 111, 219),
        ("Josh", "Nebo", "United States", "C", "1997-04-16", 213, 113, 220),
        ("Giampaolo", "Ricci", "Italy", "SF", "1991-08-11", 201, 97, 209),
    ],
    "Fenerbahce Beko": [
        ("Scottie", "Wilbekin", "United States", "PG", "1992-10-08", 185, 84, 194),
        ("Nigel", "Hayes-Davis", "United States", "SF", "1994-12-29", 201, 104, 210),
        ("Marko", "Guduric", "Serbia", "SG", "1995-11-04", 196, 95, 204),
        ("Wade", "Baldwin IV", "United States", "PG", "1996-03-27", 193, 86, 202),
        ("Devin", "Robinson", "United States", "PF", "1995-06-28", 203, 104, 212),
        ("Dyshawn", "Pierre", "Canada", "SF", "1993-03-21", 203, 102, 212),
        ("Johannes", "Thiemann", "Germany", "C", "1993-04-29", 211, 109, 218),
        ("Bonzie", "Colson", "United States", "PF", "1997-01-07", 203, 113, 211),
        ("James", "Nunnally", "United States", "SG", "1990-11-06", 201, 97, 209),
        ("Melih", "Mahmutoglu", "Turkey", "SG", "1992-07-24", 193, 90, 201),
    ],
    "Anadolu Efes": [
        ("Shane", "Larkin", "United States", "PG", "1992-07-08", 180, 79, 189),
        ("Rodrigue", "Beaubois", "France", "SG", "1988-01-18", 188, 84, 197),
        ("Tibor", "Pleiss", "Germany", "C", "1989-10-17", 216, 118, 222),
        ("Adrien", "Moerman", "France", "PF", "1991-09-16", 206, 108, 214),
        ("Vasilije", "Micic", "Serbia", "PG", "1994-01-13", 193, 86, 201),
        ("James", "Anderson", "United States", "SG", "1990-02-05", 201, 97, 210),
        ("Sertac", "Sanli", "Turkey", "PF", "1997-03-12", 203, 104, 211),
        ("Alex", "Renfroe", "United States", "PG", "1995-11-07", 185, 80, 193),
        ("Josh", "Nebo", "United States", "C", "1997-04-16", 213, 113, 220),
        ("Bugrahan", "Tuncer", "Turkey", "SG", "1998-07-14", 193, 88, 201),
    ],
    "Panathinaikos BC": [
        ("Kendrick", "Nunn", "United States", "PG", "1995-08-03", 188, 84, 197),
        ("Thomas", "Walkup", "United States", "PG", "1993-04-12", 193, 88, 202),
        ("Lorenzo", "Brown", "United States", "PG", "1990-08-26", 196, 93, 205),
        ("Ioannis", "Papapetrou", "Greece", "SF", "1994-04-04", 201, 99, 210),
        ("Mateusz", "Ponitka", "Poland", "SF", "1993-11-18", 203, 102, 212),
        ("Georgios", "Papagiannis", "Greece", "C", "1997-02-16", 218, 118, 224),
        ("Brandon", "Davies", "United States", "C", "1994-10-04", 206, 109, 214),
        ("Nemanja", "Nedovic", "Serbia", "SG", "1991-12-29", 196, 93, 204),
        ("Markus", "Howard", "United States", "PG", "1999-10-17", 178, 75, 185),
        ("Kostas", "Papanikolaou", "Greece", "SF", "1990-11-12", 203, 100, 211),
    ],
    "Olympiacos BC": [
        ("Sasha", "Vezenkov", "Bulgaria", "PF", "1995-04-23", 203, 102, 211),
        ("Giorgos", "Printezis", "Greece", "PF", "1983-05-25", 203, 104, 210),
        ("Jordan", "Theodore", "United States", "PG", "1994-09-29", 183, 77, 192),
        ("Malcolm", "Cazalon", "France", "SG", "2000-03-17", 193, 86, 202),
        ("Kostas", "Sloukas", "Greece", "PG", "1990-11-10", 193, 88, 200),
        ("Moustapha", "Fall", "Senegal", "C", "1992-07-04", 218, 108, 224),
        ("Shaquielle", "McKissic", "United States", "SF", "1993-11-05", 193, 95, 202),
        ("Elias", "Valtonen", "Finland", "SG", "2000-06-16", 196, 91, 204),
        ("Tyler", "Dorsey", "United States", "SG", "1997-04-17", 196, 93, 204),
        ("Lorentzos", "Bartzokas", "Greece", "PG", "2001-05-19", 188, 80, 196),
    ],
    "Bayern Munich Basketball": [
        ("Vladimir", "Lucic", "Serbia", "SF", "1989-04-10", 203, 102, 211),
        ("Serge", "Ibaka", "Congo", "C", "1989-09-18", 211, 113, 218),
        ("Oscar", "da Silva", "Brazil", "SF", "1996-11-08", 206, 104, 214),
        ("Isaac", "Bonga", "Germany", "SG", "2000-01-22", 203, 93, 213),
        ("Andreas", "Obst", "Germany", "SG", "1996-05-25", 196, 95, 204),
        ("Othello", "Hunter", "United States", "C", "1984-07-18", 208, 109, 215),
        ("Sylvain", "Francisco", "France", "PG", "1997-06-20", 188, 82, 197),
        ("Carsen", "Edwards", "United States", "PG", "1997-10-16", 183, 80, 191),
        ("Leon", "Kratzer", "Germany", "C", "1996-07-30", 213, 111, 219),
        ("Jalen", "Reynolds", "United States", "C", "1995-01-11", 208, 111, 215),
    ],
    "Alba Berlin": [
        ("Johannes", "Thiemann", "Germany", "C", "1993-04-29", 211, 109, 218),
        ("Marcus", "Eriksson", "Sweden", "SG", "1991-05-22", 193, 90, 201),
        ("Yovel", "Zoosman", "Israel", "SF", "1997-01-26", 201, 95, 209),
        ("Louis", "Olinde", "Germany", "PF", "1997-08-13", 203, 104, 211),
        ("Tamir", "Blatt", "Israel", "PG", "1998-11-25", 185, 82, 193),
        ("Jonas", "Mattisseck", "Germany", "PG", "2000-11-27", 193, 86, 202),
        ("Malte", "Delow", "Germany", "SG", "1999-01-06", 196, 91, 204),
        ("Jaleen", "Smith", "United States", "SG", "1997-07-26", 188, 84, 196),
        ("Sterling", "Brown", "United States", "SG", "1995-02-10", 198, 102, 207),
        ("Ben", "Lammers", "United States", "C", "1995-10-24", 211, 109, 218),
    ],
    "Partizan Mozzart Bet": [
        ("Kevin", "Punter", "United States", "SG", "1993-11-15", 193, 84, 201),
        ("Mathias", "Lessort", "France", "C", "1995-02-22", 208, 120, 215),
        ("Zeljko", "Sakic", "Serbia", "PG", "1995-06-19", 185, 79, 194),
        ("Dante", "Exum", "Australia", "PG", "1995-07-13", 193, 88, 202),
        ("Carlik", "Jones", "United States", "PG", "1998-01-31", 185, 82, 194),
        ("Trent", "Forrest", "United States", "PG", "1998-01-03", 193, 91, 201),
        ("Sterling", "Brown", "United States", "SG", "1995-02-10", 198, 102, 207),
        ("Marcus", "Lee", "United States", "PF", "1995-05-19", 208, 104, 215),
        ("Ognjen", "Jaramaz", "Serbia", "PG", "1997-02-27", 193, 86, 201),
        ("Vanja", "Marinkovic", "Serbia", "SG", "1997-06-27", 193, 88, 201),
    ],
    "Crvena Zvezda": [
        ("Nikola", "Ivanovic", "Serbia", "PG", "2001-01-11", 188, 82, 197),
        ("Joel", "Bolomboy", "United States", "PF", "1992-10-06", 208, 109, 215),
        ("Uros", "Trifunovic", "Serbia", "SG", "1992-02-03", 196, 93, 204),
        ("Matthew", "Hurt", "United States", "PF", "2001-07-13", 208, 104, 215),
        ("Ife", "Lundberg", "Denmark", "SG", "2001-12-21", 198, 93, 207),
        ("Nemanja", "Dangubic", "Serbia", "SG", "1996-05-01", 196, 93, 204),
        ("Jock", "Landale", "Australia", "C", "1995-10-19", 213, 115, 220),
        ("Filip", "Covic", "Serbia", "PG", "1995-08-22", 191, 84, 199),
        ("Dejan", "Davidovac", "Serbia", "SF", "1995-06-17", 201, 97, 209),
        ("Aleksa", "Avramovic", "Serbia", "PG", "1994-06-14", 188, 82, 196),
    ],
    "Maccabi Tel Aviv": [
        ("Wade", "Baldwin IV", "United States", "PG", "1996-03-27", 193, 86, 202),
        ("Scottie", "Wilbekin", "United States", "PG", "1992-10-08", 185, 84, 194),
        ("Yam", "Madar", "Israel", "PG", "1999-03-04", 191, 84, 199),
        ("Ante", "Zizic", "Croatia", "C", "1997-01-04", 211, 113, 218),
        ("Elijah", "Bryant", "United States", "SG", "1995-12-05", 193, 95, 201),
        ("Josh", "Nebo", "United States", "C", "1997-04-16", 213, 113, 220),
        ("Kenneth", "Ogbe", "Norway", "SF", "1993-06-21", 198, 99, 207),
        ("Deon", "Thompson", "United States", "PF", "1987-11-14", 203, 106, 211),
        ("Jalen", "Harris", "United States", "SG", "1998-12-12", 193, 86, 201),
        ("Tamir", "Blatt", "Israel", "PG", "1998-11-25", 185, 82, 193),
    ],
    "AS Monaco Basketball": [
        ("Mike", "James", "United States", "PG", "1990-10-24", 193, 88, 201),
        ("Elie", "Okobo", "France", "PG", "1997-08-11", 191, 84, 199),
        ("Donta", "Hall", "United States", "C", "1996-04-30", 208, 109, 215),
        ("Matthew", "Strazel", "France", "PG", "2002-07-25", 188, 79, 196),
        ("Jaron", "Blossomgame", "United States", "SF", "1994-04-08", 201, 102, 210),
        ("Yakuba", "Ouattara", "France", "SF", "2001-02-22", 201, 95, 209),
        ("Donatas", "Motiejunas", "Lithuania", "C", "1990-09-20", 213, 107, 219),
        ("Alpha", "Diallo", "France", "SF", "2000-09-03", 198, 97, 207),
        ("Jordan", "Lee", "United States", "PF", "1995-12-10", 203, 104, 211),
        ("Paris", "Lee", "United States", "PG", "1995-10-12", 190, 82, 198),
    ],
    "Saski Baskonia": [
        ("Chima", "Moneke", "Italy", "PF", "1997-11-20", 203, 104, 212),
        ("DJ", "Strawberry", "United States", "SG", "1991-04-09", 196, 95, 204),
        ("Pierria", "Henry", "France", "PG", "1993-12-17", 188, 82, 197),
        ("Tadas", "Sedekerskis", "Lithuania", "SF", "1998-02-05", 203, 99, 211),
        ("Ilimane", "Diop", "Spain", "C", "1996-01-23", 218, 113, 225),
        ("Luca", "Vildoza", "Argentina", "PG", "1995-11-04", 193, 84, 201),
        ("Markus", "Howard", "United States", "PG", "1999-10-17", 178, 75, 185),
        ("Jayson", "Granger", "Uruguay", "PG", "1987-10-26", 190, 84, 198),
        ("Matt", "Costello", "United States", "C", "1994-04-18", 211, 109, 218),
        ("Rolands", "Smits", "Latvia", "C", "1996-09-23", 216, 113, 222),
    ],
    "Virtus Segafredo Bologna": [
        ("Marco", "Belinelli", "Italy", "SG", "1986-03-25", 196, 93, 204),
        ("Toko", "Shengelia", "Georgia", "SF", "1991-07-04", 206, 108, 214),
        ("Daniel", "Hackett", "Italy", "PG", "1987-07-05", 193, 88, 201),
        ("Achille", "Polonara", "Italy", "SF", "1991-10-30", 203, 100, 211),
        ("Milos", "Teodosic", "Serbia", "PG", "1987-03-19", 196, 97, 204),
        ("Tornike", "Shengelia", "Georgia", "SF", "1991-07-04", 206, 108, 214),
        ("Iffe", "Lundberg", "Denmark", "SG", "2001-12-21", 198, 93, 207),
        ("Alessandro", "Pajola", "Italy", "PG", "1999-08-20", 191, 84, 199),
        ("Isaia", "Cordinier", "France", "SG", "1997-06-07", 196, 93, 204),
        ("Kyle", "Weems", "United States", "SG", "1989-05-19", 196, 95, 204),
    ],
    "Zalgiris Kaunas": [
        ("Jannick", "Faried", "United States", "PF", "1995-05-14", 206, 109, 214),
        ("Sylvain", "Francisco", "France", "PG", "1997-06-20", 188, 82, 197),
        ("Brandon", "Davies", "United States", "C", "1994-10-04", 206, 109, 214),
        ("Kendrick", "Perry", "United States", "PG", "1990-06-21", 191, 84, 200),
        ("Tai", "Webster", "New Zealand", "PG", "1994-10-24", 196, 88, 205),
        ("Martinas", "Geben", "Lithuania", "C", "1995-08-05", 211, 108, 218),
        ("Joshua", "Obiesie", "Nigeria", "SF", "1999-11-11", 201, 97, 210),
        ("Nate", "Reuvers", "United States", "PF", "1998-05-23", 211, 104, 218),
        ("Lukas", "Lekavicious", "Lithuania", "SG", "1995-01-22", 196, 91, 204),
        ("Mantas", "Kalnietis", "Lithuania", "PG", "1988-04-11", 188, 82, 196),
    ],
    "Valencia Basket": [
        ("Mike", "Tobey", "United States", "C", "1993-05-05", 213, 111, 220),
        ("Sam", "Van Rossom", "Belgium", "PG", "1987-01-04", 190, 84, 199),
        ("Klemen", "Prepelic", "Slovenia", "SG", "1993-05-20", 196, 91, 204),
        ("Jasiel", "Rivero", "Cuba", "C", "1997-03-21", 208, 108, 215),
        ("Xabi", "Lopez-Arostegui", "Spain", "SF", "1997-04-02", 201, 99, 210),
        ("Brizuela", "Dario", "Spain", "SG", "1996-09-04", 193, 90, 201),
        ("Neno", "Dimitrijevic", "Serbia", "PG", "2000-11-04", 185, 79, 193),
        ("Chris", "Jones", "United States", "PG", "1996-09-15", 190, 84, 199),
        ("Louis", "Labeyrie", "France", "C", "1993-07-23", 213, 111, 218),
        ("Sergi", "Garcia", "Spain", "PG", "1994-09-04", 188, 82, 196),
    ],
    "Paris Basketball": [
        ("TJ", "Shorts", "United States", "PG", "1999-01-12", 183, 79, 192),
        ("Matthew", "Strazel", "France", "PG", "2002-07-25", 188, 79, 196),
        ("Youssoupha", "Fall", "Senegal", "C", "2001-03-15", 218, 106, 224),
        ("Jordan", "Howard", "United States", "SG", "1996-11-08", 196, 95, 204),
        ("Zane", "Gasparini", "Italy", "SG", "1996-04-21", 198, 95, 207),
        ("Wilfried", "Yeguete", "France", "PF", "1991-05-23", 203, 104, 211),
        ("Alexandre", "Chassang", "France", "C", "1997-02-21", 213, 107, 219),
        ("Paul", "Lacombe", "France", "SG", "1990-04-01", 196, 93, 204),
        ("Maxime", "Courby", "France", "PG", "1996-05-12", 190, 84, 199),
        ("Isaïa", "Cordinier", "France", "SG", "1997-06-07", 196, 93, 204),
    ],
}


def rnd(lo, hi):
    return random.randint(lo, hi)


def make_stats(match, player, starter=True):
    in_game = starter or random.random() > 0.15
    mins = rnd(20, 38) if starter else (rnd(5, 20) if in_game else 0)
    if not in_game:
        mins = 0

    PlayerMatchStatus.objects.get_or_create(
        player=player,
        match=match,
        defaults={"in_game": in_game, "starter": starter},
    )

    if not in_game:
        return

    fg_att = rnd(4, 16)
    fg_made = rnd(0, fg_att)
    three_att = rnd(0, min(fg_att, 8))
    three_made = rnd(0, three_att)
    ft_att = rnd(0, 8)
    ft_made = rnd(0, ft_att)
    pts = fg_made * 2 + three_made + ft_made

    PlayerStats.objects.get_or_create(
        player=player,
        match=match,
        defaults={
            "points": pts,
            "rebounds": rnd(0, 12),
            "assists": rnd(0, 10),
            "steals": rnd(0, 4),
            "blocks": rnd(0, 4),
            "turnovers": rnd(0, 5),
            "fouls": rnd(0, 5),
            "minutes_played": mins,
            "fg_made": fg_made,
            "fg_attempted": fg_att,
            "three_pt_made": three_made,
            "three_pt_attempted": three_att,
            "ft_made": ft_made,
            "ft_attempted": ft_att,
        },
    )


class Command(BaseCommand):
    help = "Seed database with NBA and Euroleague data for seasons 2024/25 and 2025/26"

    def handle(self, *args, **options):
        random.seed(42)
        self.stdout.write("Starting seed...")

        # ── Countries ─────────────────────────────────────────────────────────
        self.stdout.write("Creating countries...")
        country_map = {}
        for name in COUNTRIES:
            obj, _ = Country.objects.get_or_create(name=name)
            country_map[name] = obj

        # ── Cities & Halls ────────────────────────────────────────────────────
        self.stdout.write("Creating cities and halls...")
        city_map = {}    # city_name -> City
        hall_map = {}    # city_name -> Hall

        for country_name, entries in CITIES_HALLS.items():
            country = country_map.get(country_name)
            if not country:
                continue
            for city_name, hall_name, capacity in entries:
                city, _ = City.objects.get_or_create(
                    name=city_name,
                    defaults={"country": country},
                )
                city_map[city_name] = city

                hall, _ = Hall.objects.get_or_create(
                    name=hall_name,
                    defaults={"city": city, "capacity": capacity},
                )
                hall_map[city_name] = hall

        # ── Seasons ───────────────────────────────────────────────────────────
        self.stdout.write("Creating seasons...")
        season_2425, _ = Season.objects.get_or_create(
            name="2024/2025",
            defaults={"start_date": date(2024, 10, 1), "end_date": date(2025, 6, 30)},
        )
        season_2526, _ = Season.objects.get_or_create(
            name="2025/2026",
            defaults={"start_date": date(2025, 10, 1), "end_date": date(2026, 6, 30)},
        )
        seasons = [season_2425, season_2526]

        # ── Positions ─────────────────────────────────────────────────────────
        self.stdout.write("Creating positions...")
        pos_map = {}
        for pos_name in ["PG", "SG", "SF", "PF", "C"]:
            obj, _ = Position.objects.get_or_create(name=pos_name)
            pos_map[pos_name] = obj

        # ── Leagues ───────────────────────────────────────────────────────────
        self.stdout.write("Creating leagues...")
        nba, _ = League.objects.get_or_create(name="NBA")
        euroleague, _ = League.objects.get_or_create(name="Euroleague")

        # ── Match statuses ────────────────────────────────────────────────────
        status_finished, _ = Status.objects.get_or_create(name="Finished")
        status_scheduled, _ = Status.objects.get_or_create(name="Scheduled")
        Status.objects.get_or_create(name="Live")

        # ── Teams ─────────────────────────────────────────────────────────────
        self.stdout.write("Creating teams...")
        team_map = {}

        all_team_defs = [
            (NBA_TEAMS, nba),
            (EUROLEAGUE_TEAMS, euroleague),
        ]

        for team_defs, league_obj in all_team_defs:
            for team_name, city_name, country_name in team_defs:
                city = city_map.get(city_name)
                if not city:
                    country = country_map.get(country_name)
                    if not country:
                        country, _ = Country.objects.get_or_create(name=country_name)
                        country_map[country_name] = country
                    city, _ = City.objects.get_or_create(
                        name=city_name,
                        defaults={"country": country},
                    )
                    city_map[city_name] = city

                team, _ = Team.objects.get_or_create(
                    name=team_name,
                    defaults={"city": city},
                )
                team_map[team_name] = team

        # ── LeagueTeam ────────────────────────────────────────────────────────
        self.stdout.write("Creating league-team memberships...")

        def create_league_teams(team_defs, league_obj, season_obj, wins_range, losses_range):
            for team_name, _, _ in team_defs:
                team = team_map[team_name]
                LeagueTeam.objects.get_or_create(
                    league=league_obj,
                    team=team,
                    season=season_obj,
                    defaults={
                        "win": rnd(*wins_range),
                        "loss": rnd(*losses_range),
                    },
                )

        create_league_teams(NBA_TEAMS, nba, season_2425, (20, 60), (20, 60))
        create_league_teams(NBA_TEAMS, nba, season_2526, (0, 45), (0, 45))
        create_league_teams(EUROLEAGUE_TEAMS, euroleague, season_2425, (10, 30), (10, 30))
        create_league_teams(EUROLEAGUE_TEAMS, euroleague, season_2526, (0, 15), (0, 15))

        # ── Players ───────────────────────────────────────────────────────────
        self.stdout.write("Creating players...")
        player_map = {}  # team_name -> [Player]

        all_player_defs = {**NBA_PLAYERS, **EUROLEAGUE_PLAYERS}

        for team_name, players in all_player_defs.items():
            team = team_map.get(team_name)
            if not team:
                continue
            player_map[team_name] = []
            for first, last, country_name, pos_name, dob_str, height, weight, wingspan in players:
                country = country_map.get(country_name)
                if not country:
                    country, _ = Country.objects.get_or_create(name=country_name)
                    country_map[country_name] = country

                player, _ = Player.objects.get_or_create(
                    first_name=first,
                    last_name=last,
                    defaults={
                        "nationality": country,
                        "team": team,
                        "position": pos_map.get(pos_name),
                        "date_of_birth": date.fromisoformat(dob_str),
                        "height_cm": height,
                        "weight_kg": weight,
                        "wingspan_cm": wingspan,
                    },
                )
                player_map[team_name].append(player)

        # ── Matches & Stats ───────────────────────────────────────────────────
        self.stdout.write("Creating matches and player stats...")

        def generate_matches(team_defs, league_obj, season_obj, base_date, num_finished, num_scheduled):
            team_names = [t[0] for t in team_defs]
            city_by_team = {t[0]: t[1] for t in team_defs}
            pairs = []
            random.shuffle(team_names)
            for i in range(0, len(team_names) - 1, 2):
                pairs.append((team_names[i], team_names[i + 1]))
            # fill up to num_finished + num_scheduled total games
            while len(pairs) < num_finished + num_scheduled:
                a, b = random.sample(team_names, 2)
                pairs.append((a, b))

            for idx, (home_name, away_name) in enumerate(pairs[:num_finished + num_scheduled]):
                home_team = team_map[home_name]
                away_team = team_map[away_name]
                match_dt = base_date + timedelta(days=idx * 5)
                is_finished = idx < num_finished
                status = status_finished if is_finished else status_scheduled
                hall = hall_map.get(city_by_team.get(home_name))

                match, created = Match.objects.get_or_create(
                    home_team=home_team,
                    away_team=away_team,
                    league=league_obj,
                    season=season_obj,
                    match_date=timezone.make_aware(
                        datetime.combine(match_dt, datetime.min.time().replace(hour=19, minute=30))
                    ),
                    defaults={
                        "status": status,
                        "hall": hall,
                        "home_score": rnd(85, 130) if is_finished else None,
                        "away_score": rnd(85, 130) if is_finished else None,
                    },
                )

                if created and is_finished:
                    home_players = player_map.get(home_name, [])
                    away_players = player_map.get(away_name, [])
                    starters_h = home_players[:5]
                    bench_h = home_players[5:]
                    starters_a = away_players[:5]
                    bench_a = away_players[5:]
                    for p in starters_h:
                        make_stats(match, p, starter=True)
                    for p in bench_h:
                        make_stats(match, p, starter=False)
                    for p in starters_a:
                        make_stats(match, p, starter=True)
                    for p in bench_a:
                        make_stats(match, p, starter=False)

        # NBA 2024/25 – lots of finished matches, few scheduled
        generate_matches(NBA_TEAMS, nba, season_2425, date(2024, 10, 22), num_finished=40, num_scheduled=5)
        # NBA 2025/26 – season just started, many scheduled
        generate_matches(NBA_TEAMS, nba, season_2526, date(2025, 10, 21), num_finished=10, num_scheduled=35)

        # Euroleague 2024/25
        generate_matches(EUROLEAGUE_TEAMS, euroleague, season_2425, date(2024, 10, 3), num_finished=25, num_scheduled=5)
        # Euroleague 2025/26
        generate_matches(EUROLEAGUE_TEAMS, euroleague, season_2526, date(2025, 10, 2), num_finished=8, num_scheduled=22)

        self.stdout.write(self.style.SUCCESS("Seed complete!"))
        self.stdout.write(f"  Countries : {Country.objects.count()}")
        self.stdout.write(f"  Cities    : {City.objects.count()}")
        self.stdout.write(f"  Halls     : {Hall.objects.count()}")
        self.stdout.write(f"  Seasons   : {Season.objects.count()}")
        self.stdout.write(f"  Teams     : {Team.objects.count()}")
        self.stdout.write(f"  Players   : {Player.objects.count()}")
        self.stdout.write(f"  Leagues   : {League.objects.count()}")
        self.stdout.write(f"  LeagueTeam: {LeagueTeam.objects.count()}")
        self.stdout.write(f"  Matches   : {Match.objects.count()}")
        self.stdout.write(f"  PlayerStats: {PlayerStats.objects.count()}")
        self.stdout.write(f"  PlayerMatchStatus: {PlayerMatchStatus.objects.count()}")
