from csv_utils import *
from init import create_leaderboard
from problem_files import get_attempts
from problems_table import get_difficulty, get_name
from constants import GlobalLeaderboardStruct, \
    ProblemFileStruct, DIFFICULTY_MULTIPLIER, ProblemHeaders, GlobalHeaders
from discord_funcs import reply_to_message

''' LEADERBOARDS '''
# data/globalLeaderboard.csv
# [username, points, problems tried, average percentage]


def display_problem_leader_board(message, problem_id):
    out = "Leaderboard for Problem {}: ".format(problem_id)
    out += get_name(problem_id) + "\n"
    out += generate_problem_leader_board_message(problem_id)
    reply_to_message(message, out)


def generate_problem_leader_board_message(problem_id):
    attempts = get_attempts(problem_id)
    attempts = sort_problem_leader_board(attempts)
    points = calculate_points(attempts, get_difficulty(problem_id))
    headers = get_problem_leader_board_headers()
    header_sizes = get_problem_leader_board_header_sizes(headers, attempts, points)
    table = create_problem_header(headers, header_sizes)
    for i in range(0, len(attempts)):
        table += create_attempt_row(attempts[i], header_sizes, i + 1, points[i])

    table += "\n"
    return table


def create_problem_header(headers, header_sizes):
    header = ""
    for i in range(0, len(headers)):
        (gap, offset) = divmod(header_sizes[i] - len(headers[i]) - 2, 2)
        header += ' ' * gap + headers[i] + ' ' * (gap + offset)
        if i + 1 != len(headers):
            header += "|"

    dashes = '-' * len(headers)
    header = header + "\n" + dashes + "\n"
    return header


def create_attempt_row(attempt, header_sizes, rank, points):
    row = ""
    body = str(rank)
    row += add_padding(body, header_sizes[ProblemHeaders.RANK])

    body = attempt[ProblemFileStruct.NAME]
    row += add_padding(body, header_sizes[ProblemHeaders.NAME])

    body = attempt[ProblemFileStruct.PERCENT] + "%"
    row += add_padding(body, header_sizes[ProblemHeaders.PERCENT])

    body = "O(" + attempt[ProblemFileStruct.COMPLEXITY] + ")"
    row += add_padding(body, header_sizes[ProblemHeaders.BIG_O])

    body = attempt[ProblemFileStruct.LANGUAGE]
    row += add_padding(body, header_sizes[ProblemHeaders.LANGUAGE])

    body = points
    row += add_padding(body, header_sizes[ProblemHeaders.POINTS])

    row += "\n"
    return row


def add_padding(body, header_size):
    return body + ' ' * (1 + header_size - len(body))


def get_problem_leader_board_header_sizes(headers, attempts, max_points):
    header_sizes = [len(h) + 4 for h in headers]
    for a in attempts:
        header_sizes = compare_problem_header_size(a, header_sizes)

    header_sizes[ProblemHeaders.POINTS] = max(len(str(max_points)),
                                              header_sizes[ProblemHeaders.POINTS])
    return header_sizes


def compare_problem_header_size(entry, headers):
    headers[ProblemHeaders.NAME] = max(1 + entry[ProblemFileStruct.NAME],
                                       headers[ProblemHeaders.NAME])
    headers[ProblemHeaders.BIG_O] = max(4 + entry[ProblemFileStruct.COMPLEXITY],
                                       headers[ProblemHeaders.BIG_O])
    headers[ProblemHeaders.LANGUAGE] = max(1 + entry[ProblemFileStruct.LANGUAGE],
                                       headers[ProblemHeaders.LANGUAGE])
    return headers


def get_problem_leader_board_headers():
    headers = ["" for _ in range(0, len(ProblemHeaders))]
    headers[ProblemHeaders.RANK] = "Rank"
    headers[ProblemHeaders.NAME] = "Name"
    headers[ProblemHeaders.PERCENT] = "Percent"
    headers[ProblemHeaders.BIG_O] = "Big O"
    headers[ProblemHeaders.LANG] = "Language"
    headers[ProblemHeaders.POINTS] = "Points"
    return headers


def display_global_leader_board(message):
    out = "Global Leaderboard:"
    out += generate_global_leader_board_message()
    reply_to_message(message, out)


def generate_global_leader_board_message():
    leader_board = get_global_leader_board()
    leader_board = sort_global_leader_board(leader_board)
    headers = get_global_leader_board_headers()
    header_sizes = get_global_leader_board_header_sizes(headers)

    table = create_global_header(headers, header_sizes)
    for i in range(0, len(leader_board)):
        table += create_global_row(leader_board[i], header_sizes, i + 1)

    table += "\n"
    return table


def create_global_row(entry, header_sizes, rank):
    row = ""

    body = str(rank) + " |"
    row += add_padding(body, header_sizes[GlobalHeaders.RANK])

    body = entry[GlobalLeaderboardStruct.NAME]
    row += add_padding(body, header_sizes[GlobalHeaders.NAME])

    body = entry[GlobalLeaderboardStruct.POINTS]
    row += add_padding(body, header_sizes[GlobalHeaders.POINTS])

    body = entry[GlobalLeaderboardStruct.NO_PROBLEMS]
    row += add_padding(body, header_sizes[GlobalHeaders.PROBLEMS_TRIED])

    body = entry[GlobalLeaderboardStruct.AVERAGE_PERCENT]
    row += add_padding(body, header_sizes[GlobalHeaders.AVERAGE_PERCENT])

    row += "\n"
    return row


def get_global_leader_board_headers():
    headers = ["" for _ in range(0, len(GlobalHeaders))]
    headers[GlobalHeaders.RANK] = "   |"
    headers[GlobalHeaders.NAME] = "Name"
    headers[GlobalHeaders.POINTS] = "Points"
    headers[GlobalHeaders.PROBLEMS_TRIED] = "#Problems"
    headers[GlobalHeaders.AVERAGE_PERCENT] = "Average %"
    return headers


def get_global_leader_board_header_sizes(headers, board):
    header_sizes = [len(h) + 2 for h in headers]
    header_sizes[GlobalHeaders.RANK] = 4
    for entry in board:
        header_sizes[GlobalHeaders.NAME] = max(header_sizes[GlobalHeaders.NAME],
                                               1 + len(entry[GlobalLeaderboardStruct.NAME]))
    max_points = max([b[GlobalLeaderboardStruct.POINTS] for b in board])
    header_sizes[GlobalHeaders.POINTS] = max(header_sizes[GlobalHeaders.POINTS],
                                             1 + len(str(max_points)))
    max_problems = max(([b[GlobalLeaderboardStruct.NO_PROBLEMS] for b in board]))
    header_sizes[GlobalHeaders.PROBLEMS_TRIED] = max(header_sizes[GlobalHeaders.PROBLEMS_TRIED],
                                                     1 + len(str(max_problems)))
    return header_sizes


def create_global_header(headers, header_sizes):
    header = headers[GlobalHeaders.RANK]
    for i in range(1, len(headers)):
        (gap, offset) = divmod(header_sizes[i] - len(headers[i]), 2)
        header += ' ' * gap + headers[i] + ' ' * (gap + offset)
    return header


def save_global_board(board):
    overwrite_rows(get_global_leader_board_file_name(), board)


def remove_attempt_global_leader_board(board, name, percent, points):
    user = get_user_entry_board(board, name)
    new_user = remove_attempt_from_user(user, percent, points)
    new_board = replace_user_entry_board(board, new_user)
    sorted_board = sort_global_leader_board(new_board)
    return sorted_board


def add_attempt_global_leader_board(board, name, percent, points):
    user = get_user_entry_board(board, name)
    new_user = add_attempt_to_user(user, percent, points)
    new_board = replace_user_entry_board(board, new_user)
    sorted_board = sort_global_leader_board(new_board)
    return sorted_board


def add_attempt_to_user(user, percent, points):
    user[GlobalLeaderboardStruct.POINTS] += points
    old_total_percent = user[GlobalLeaderboardStruct.AVERAGE_PERCENT] * user[GlobalLeaderboardStruct.NO_PROBLEMS]
    new_total_percent = old_total_percent + percent
    new_percent = new_total_percent / (user[GlobalLeaderboardStruct.NO_PROBLEMS] + 1.0)
    user[GlobalLeaderboardStruct.AVERAGE_PERCENT] = new_percent
    user[GlobalLeaderboardStruct.NO_PROBLEMS] += 1
    return user


def remove_attempt_from_user(user, percent, points):
    user[GlobalLeaderboardStruct.POINTS] -= points
    old_total_percent = user[GlobalLeaderboardStruct.AVERAGE_PERCENT] * user[GlobalLeaderboardStruct.NO_PROBLEMS]
    new_total_percent = old_total_percent - percent
    try:
        new_percent = new_total_percent / (user[GlobalLeaderboardStruct.NO_PROBLEMS])
    except ZeroDivisionError:
        new_percent = 0
    user[GlobalLeaderboardStruct.AVERAGE_PERCENT] = new_percent
    user[GlobalLeaderboardStruct.NO_PROBLEMS] -= 1
    return user


def get_user_entry_board(board, name):
    entries = [b for b in board if b[GlobalLeaderboardStruct.NAME] == name]
    if len(entries) != 0:
        return entries[0]
    else:
        return get_new_global_leader_board_entry(name)


def replace_user_entry_board(board, new_version):
    for i in range(0, len(board)):
        if board[i][GlobalLeaderboardStruct.NAME] == new_version[GlobalLeaderboardStruct.NAME]:
            board[i] = new_version
            return board
        return board


def get_new_global_leader_board_entry(name):
    return [name, 0, 0, 0]


# Assumes problem_id exists
def get_problem_leader_board(problem_id):
    attempts = get_attempts(problem_id)
    return sort_problem_leader_board(attempts)


def sort_problem_leader_board(attempts):
    attempts.sort(key=lambda x: x[ProblemFileStruct.PERCENT])
    return attempts


def sort_global_leader_board(leader_board):
    leader_board.sort(key=lambda x: (x[GlobalLeaderboardStruct.POINTS], x[GlobalLeaderboardStruct.AVERAGE_PERCENT]))
    return leader_board


# Returns {name: points}
def calculate_points(attempts, diff):
    attempts = sort_problem_leader_board(attempts)
    filtered_attempts = remove_same_percents(attempts)
    positions = {}
    for i in range(0, len(filtered_attempts)):
        positions[filtered_attempts[i][ProblemFileStruct.PERCENT]] = i
    result = {}
    for user in attempts:
        position_points = (len(filtered_attempts) -
                           positions[user[ProblemFileStruct.PERCENT]])
        points = position_points * DIFFICULTY_MULTIPLIER[diff]
        result[user[ProblemFileStruct.NAME]] = points

    return result


def remove_same_percents(attempts):
    seen = set()
    result = []
    for a in attempts:
        if a[ProblemFileStruct.PERCENT] not in seen:
            result.append(a)
            seen.add(a[ProblemFileStruct.PERCENT])
    return result


def get_global_leader_board():
    try:
        return read_csv(get_global_leader_board_file_name())
    except FileNotFoundError:
        create_leaderboard()
        get_global_leader_board()


def get_global_leader_board_file_name():
    return "data/globalLeaderboard.csv"
