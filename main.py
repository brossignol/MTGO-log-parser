import os
from log_parser import update_player_map, parse_started_event, update_standings


def main(path, out_path, filters):
    with open(path) as file:
        log = file.readlines()

    challenges = parse_started_event(log)
    update_player_map(log, challenges)
    update_standings(log, challenges)

    for token, challenge in challenges.items():
        if not filters or any(f in challenge['name'] for f in filters):
            print(challenge['name'])
            path = os.path.join(out_path, challenge['name'] + '.csv').replace(' ', '_')
            with open(path, 'w') as file:
                df = challenge['standings']
                for row in [df, *zip(*df.values())]:
                    file.write(','.join(map(str, row)) + '\n')

            print(make_console_link(path))


def get_mtgo_log(mtgo_path):
    # return last modified log
    logs = []
    for dirpath, dirnames, filenames in os.walk(mtgo_path):
        for file in filenames:
            if file == 'mtgo.log':
                logs.append(os.path.join(dirpath, file))

    return max(logs, key=lambda f: os.stat(f).st_mtime)


def make_console_link(path: str):
    return r'file:///' + os.path.abspath(path).replace('\\', '/')


if __name__ == '__main__':
    mtgo_path = os.path.expanduser('~') + r'\AppData\Local\Apps\2.0'
    path_to_log = get_mtgo_log(mtgo_path)
    out_folder = 'data'
    filters = []
    os.makedirs(out_folder, exist_ok=True)
    main(path_to_log, out_folder, filters)
