from bs4 import BeautifulSoup
import urllib2
import re


print "Gathering up to date players stats..."
# scrape hockey-reference for updated stats
link = urllib2.urlopen('http://www.hockey-reference.com/leagues/NHL_2017_goalies.html')
soup = BeautifulSoup(link, 'lxml')
i = 0
player_stats = []
players = []
w = open('goalie.txt', 'w')
header = '\t'.join([
            "Player", "Age", "Tm", "Games Played", "Games Started",
            "Wins", "Losses", "Ties plus OT/SO Losses", "Goals Against", "Shots Against",
            "Saves", "Save Percentage", "Goals Against Average",
            "Shutouts", "Minutes", "Quality Starts", "Quality Start Percentage",
            "Really Bad Starts", "Goals Allowed Adjusted",
            "Goals Saved Above Average", "Goals", "Assists", "Points", "Penalties in Minutes"
])
w.write(header + '\n')
for row in soup.find_all('td', {'data-stat': re.compile(r'.+')}):
    player_stats.append(row.text.strip())
    i += 1
    if i == 24:
        i = 0
        players.extend([player_stats])
        player_stats = []
for player in players:
    w.write('\t'.join(player) + '\n')
w.close()
