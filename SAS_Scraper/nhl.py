from bs4 import BeautifulSoup
import urllib2
import argparse
import re
import time


def get_stats():
    # scrape hockey-reference for updated stats
    link = urllib2.urlopen('http://www.hockey-reference.com/leagues/NHL_2017_skaters.html')
    soup = BeautifulSoup(link, 'lxml')
    i = 0
    player_stats = []
    players = []
    w = open('players.txt', 'w')
    header = '\t'.join([
        "Player", "Age", "Pos", "Tm", "Games Played", "Goals",
        "Assists", "Points", "Plus/Minus", "Penalties in Minutes",
        "Even Strength Goals", "Power Play Goals", "Short-Handed Goals",
        "Game-Winning Goals", "Even Strength Assists", "Power Play Assists",
        "Short-Handed Assists", "Shots", "Shooting Percentage", "Time on Ice",
        "Average Time on Ice", "Blocks", "Hits",
        "Faceoff Wins", "Faceoff Losses", "Faceoff Percentage"
    ])
    w.write(header + '\n')
    for row in soup.find_all('td', {'data-stat': re.compile(r'.+')}):
        player_stats.append(row.text.strip())
        i += 1
        if i == 26:
            i = 0
            players.extend([player_stats])
            player_stats = []
    for player in players:
        w.write('\t'.join(player) + '\n')
    w.close()


def get_advanced_stats():
    # scrape hockey-reference for updated stats
    link = urllib2.urlopen('http://www.hockey-reference.com/leagues/NHL_2017_skaters-advanced.html')
    soup = BeautifulSoup(link, 'lxml')
    i = 0
    player_stats = []
    players = []
    w = open('players_advanced.txt', 'w')
    header = '\t'.join([
            "Player", "Age", "Tm", "Pos", "Games Played", "Corsi For", "Corsi Against",
            "Corsi For %", "Relative Corsi For %", "Fenwick For", "Fenwick Against", "Fenwick For %",
            "Fenwick Rel", "Team On-Ice Shooting Percentage", "Team On-Ice Save Percentage",
            "PDO", "Offensive Zone Start %", "Defensive Zone Start %", "TOI/60 in All SituationsTime on Ice per 60 minutes",
            "TOI/60 at Even StrengthTime on Ice per 60 minutes", "Takeaways",
            "Giveaways", "Expected +/-", "Total shots attempted in all situations", "Percentage of shots taken that go on net"
    ])
    w.write(header + '\n')
    for row in soup.find_all('td', {'data-stat': re.compile(r'.+')}):
        player_stats.append(row.text.strip())
        i += 1
        if i == 25:
            i = 0
            players.extend([player_stats])
            player_stats = []
    for player in players:
        w.write('\t'.join(player) + '\n')
    w.close()


def get_goalie_stats():
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Team File', type=str,
                        required=True)

    args = parser.parse_args()
    team = args.input

    print "Initiating program..."
    start_time = time.time()
    # clean up the player inputs
    team_list = []
    with open(team) as f:
        for line in f:
            line = line.strip()
            team_list.append(line)
    f.close()

    print "Gathering up to date players stats..."
    get_stats()
    get_advanced_stats()
    get_goalie_stats()

    print "Writing output..."
    # aggregate team stats into file
    stats = []
    w = open('team_stats.txt', 'w')
    with open('players.txt') as f:
        header = f.readline()
        w.write(header)
        for line in f:
            player = line.strip().split('\t')[0]
            if player in team_list:
                w.write(line)
    f.close()
    with open('players_advanced.txt') as f:
        header = f.readline()
        w.write(header)
        for line in f:
            player = line.strip().split('\t')[0]
            if player in team_list:
                w.write(line)
    f.close()
    with open('goalie.txt') as f:
        header = f.readline()
        w.write(header)
        for line in f:
            player = line.strip().split('\t')[0]
            if player in team_list:
                w.write(line)
    f.close()
    w.close()
    print 'team_stats.txt written in %s seconds' % round((time.time() - start_time), 4)


if __name__ == '__main__':
    main()
