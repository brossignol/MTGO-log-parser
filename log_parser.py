import json


def parse_line(line):
    i = line.find('{')
    j = line[::-1].find('}')
    s = line[i:-j + 1]
    if s.count('{') > s.count('}'):
        s += '}'  # sometime the last parenthesis is missing
    return json.JSONDecoder().decode(s)


def get_player_map(e):
    player_map = {p['LoginID']: p['PlayerName'] for p in e["Players"]}
    player_map[-99] = 'Bye'
    return player_map


def get_standing_at_round(rd, player_map):
    n = len(rd['Results'])  # n_player
    n_round = rd.get('Round', rd.get('Number'))
    df = {'Rank': [''] * n, 'Name': [''] * n, 'Wins': [''] * n, 'Losses': [''] * n}

    for i in range(1, n_round + 1):
        df[f'R{i}'] = [''] * n
        df[f'R{i}w'] = [''] * n
        df[f'R{i}l'] = [''] * n

    for player in rd['Results']:
        i = player['Rank'] - 1
        df['Rank'][i] = i + 1
        df['Name'][i] = player_map[player['LoginID']]
        df['Wins'][i] = 0
        df['Losses'][i] = 0

        for opponent in player['OpponentResults']:
            j = n_round - opponent['Round'] + 1
            df[f'R{j}'][i] = player_map[opponent['LoginID']]
            df[f'R{j}w'][i] = opponent['Win']
            df[f'R{j}l'][i] = opponent['Loss']

            if opponent['Bye'] or opponent['Win'] > opponent['Loss']:
                df['Wins'][i] += 1
            else:
                df['Losses'][i] += 1
    return df


def parse_started_event(log):
    # load already started event
    challenges = {}
    for line in log:
        if 'PremiereEventSyncData":{' in line:
            e = parse_line(line)
            if len(e["Players"]) == 0:
                continue
            rounds = e["PremiereEventSyncData"]['TournamentSyncData']['Rounds']
            player_map = get_player_map(e)

            challenge = {'name': e['Description'] + '_' + e['StartDate'][:13], 'player_map': player_map}
            challenges[e['EventToken']] = challenge

            finished = [rd for rd in rounds if rd['Results']]
            if len(finished) > 0:
                challenge['standings'] = get_standing_at_round(finished[-1], player_map)
            else:
                challenge['standings'] = {}

    return challenges


def update_player_map(log, challenges):
    # get player map from round start message
    for line in log:
        if 'FlsTournamentRoundInfoMessage' in line and 'Matches' in line:
            e = parse_line(line)

            challenge = challenges.get(e['Token'])
            if not challenge:
                continue

            for match in e['Round']['Matches']:
                for player in match['Players']:
                    if player['LoginID'] not in challenge['player_map']:
                        challenge['player_map'][player['LoginID']] = player['PlayerName']


def update_standings(log, challenges):
    # get standings from round results
    for line in log:
        if 'FlsTournamentRoundResultMessage' in line and 'Results' in line:
            e = parse_line(line)

            challenge = challenges.get(e['Token'])
            if not challenge:
                continue

            challenge['standings'] = get_standing_at_round(e, challenge['player_map'])