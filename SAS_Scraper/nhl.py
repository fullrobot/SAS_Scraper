from bs4 import BeautifulSoup
import urllib2
import argparse
import re
import time


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

    print "Writing output..."
    # aggregate team stats into file
    stats = []
    w = open('team_stats.txt', 'w')
    with open('players.txt') as f:
        header = f.readline()
        w.write(header + '\n')
        for line in f:
            player = line.strip().split('\t')[0]
            if player in team_list:
                w.write(line)
    w.close()
    print 'team_stats.txt written in %s seconds' % round((time.time() - start_time), 4)


if __name__ == '__main__':
    main()
