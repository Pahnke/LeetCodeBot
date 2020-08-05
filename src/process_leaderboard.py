import csv_utils
import init
import problem_files
import problems_table
import constants
import discord_funcs

''' LEADERBOARDS '''
# data/globalLeaderboard.csv
# [username, points, problems tried, average percentage]


async def display_problem_leader_board(message, problem_id):
    out = "Leaderboard for Problem {}: {}\n".format(problem_id, problems_table.get_name(problem_id))
    out += "```" + generate_problem_leader_board_message(problem_id) + "```"
    await discord_funcs.reply_to_message(message, out)


def generate_problem_leader_board_message(problem_id):
    attempts = problem_files.get_attempts(problem_id)
    attempts = sort_problem_leader_board(attempts)
    points = calculate_points(attempts, problems_table.get_difficulty(problem_id))
    headers = get_problem_leader_board_headers()
    header_sizes = get_problem_leader_board_header_sizes(headers, attempts, points)
    table = create_problem_header(headers, header_sizes)
    rank = 1
    for i in range(0, len(attempts) - 1):
        table += create_attempt_row(attempts[i], header_sizes, rank,
                                    points[attempts[i][constants.ProblemFileStruct.NAME.value]])
        if attempts[i][constants.ProblemFileStruct.PERCENT.value] != attempts[i + 1][constants.ProblemFileStruct.PERCENT.value]:
            rank += 1
    if len(attempts) != 0:
        last = attempts[len(attempts) - 1]
        table += create_attempt_row(last, header_sizes, rank, points[last[constants.ProblemFileStruct.NAME.value]])
    table += "\n"
    return table


def create_problem_header(headers, header_sizes):
    header = ""
    for i in range(0, len(headers)):
        (gap, offset) = divmod(header_sizes[i] - len(headers[i]), 2)
        header += ' ' * gap + headers[i] + ' ' * (gap + offset)
        if i + 1 != len(headers):
            header += "|"

    dashes = '-' * len(header)
    header = header + "\n" + dashes + "\n"
    return header


def create_attempt_row(attempt, header_sizes, rank, points):
    row = ""
    body = str(rank)
    row += add_padding_left_align(body, header_sizes[constants.ProblemHeaders.RANK.value])

    body = attempt[constants.ProblemFileStruct.NAME.value]
    row += add_padding_left_align(body, header_sizes[constants.ProblemHeaders.NAME.value])

    body = format(attempt[constants.ProblemFileStruct.PERCENT.value], ".2f") + "%"
    row += add_padding_left_align(body, header_sizes[constants.ProblemHeaders.PERCENT.value])

    body = "O(" + attempt[constants.ProblemFileStruct.COMPLEXITY.value] + ")"
    row += add_padding_left_align(body, header_sizes[constants.ProblemHeaders.BIG_O.value])

    body = attempt[constants.ProblemFileStruct.LANGUAGE.value]
    row += add_padding_left_align(body, header_sizes[constants.ProblemHeaders.LANGUAGE.value])

    body = format(points, ".2f")
    row += add_padding_left_align(body, header_sizes[constants.ProblemHeaders.POINTS.value])

    row += "\n"
    return row


def add_padding_left_align(body, header_size):
    return body + ' ' * (1 + header_size - len(body))


def get_problem_leader_board_header_sizes(headers, attempts, points):
    header_sizes = [len(h) + 3 for h in headers]
    header_sizes[constants.ProblemHeaders.POINTS.value] = 1 + len(headers[constants.ProblemHeaders.POINTS.value])
    for a in attempts:
        header_sizes = compare_problem_header_size(a, header_sizes)

    max_points = max([0] + [points[name] for name in points])
    header_sizes[constants.ProblemHeaders.POINTS.value] = max(len(str(max_points)),
                                              header_sizes[constants.ProblemHeaders.POINTS.value])
    return header_sizes


def compare_problem_header_size(entry, headers):
    headers[constants.ProblemHeaders.NAME.value] = max(2 + len(entry[constants.ProblemFileStruct.NAME.value]),
                                       headers[constants.ProblemHeaders.NAME.value])
    headers[constants.ProblemHeaders.BIG_O.value] = max(4 + len(entry[constants.ProblemFileStruct.COMPLEXITY.value]),
                                       headers[constants.ProblemHeaders.BIG_O.value])
    headers[constants.ProblemHeaders.LANGUAGE.value] = max(1 + len(entry[constants.ProblemFileStruct.LANGUAGE.value]),
                                       headers[constants.ProblemHeaders.LANGUAGE.value])
    return headers


def get_problem_leader_board_headers():
    headers = ["" for _ in range(0, len(constants.ProblemHeaders))]
    headers[constants.ProblemHeaders.RANK.value] = "Rank"
    headers[constants.ProblemHeaders.NAME.value] = "Name"
    headers[constants.ProblemHeaders.PERCENT.value] = "Percent"
    headers[constants.ProblemHeaders.BIG_O.value] = "Big O"
    headers[constants.ProblemHeaders.LANGUAGE.value] = "Language"
    headers[constants.ProblemHeaders.POINTS.value] = "Points"
    return headers


async def display_global_leader_board(message):
    out = "Global Leaderboard:\n"
    out += "```" + generate_global_leader_board_message() + "```"
    await discord_funcs.reply_to_message(message, out)


def generate_global_leader_board_message():
    leader_board = get_global_leader_board()
    leader_board = sort_global_leader_board(leader_board)
    headers = get_global_leader_board_headers()
    header_sizes = get_global_leader_board_header_sizes(headers, leader_board)

    table = create_global_header(headers, header_sizes)
    rank = 1
    for i in range(0, len(leader_board) - 1):
        table += create_global_row(leader_board[i], header_sizes, rank)
        if (leader_board[i][constants.GlobalLeaderboardStruct.POINTS.value]
                != leader_board[i + 1][constants.GlobalLeaderboardStruct.POINTS.value] or
            leader_board[i][constants.GlobalLeaderboardStruct.AVERAGE_PERCENT.value] !=
                leader_board[i + 1][constants.GlobalLeaderboardStruct.AVERAGE_PERCENT.value]):
            rank += 1
    if len(leader_board) != 0:
        table += create_global_row(leader_board[len(leader_board) - 1], header_sizes, rank)

    table += "\n"
    return table


def create_global_row(entry, header_sizes, rank):
    row = ""

    body = str(rank)
    row += add_padding_left_align(body, header_sizes[constants.GlobalHeaders.RANK.value] - 2)
    row += "| "

    body = entry[constants.GlobalLeaderboardStruct.NAME.value]
    row += add_padding_center(body, header_sizes[constants.GlobalHeaders.NAME.value])

    body = format(entry[constants.GlobalLeaderboardStruct.POINTS.value], ".2f")
    row += add_padding_center(body, header_sizes[constants.GlobalHeaders.POINTS.value])

    body = format(entry[constants.GlobalLeaderboardStruct.NO_PROBLEMS.value], ".0f")
    row += add_padding_center(body, header_sizes[constants.GlobalHeaders.PROBLEMS_TRIED.value])

    body = format(entry[constants.GlobalLeaderboardStruct.AVERAGE_PERCENT.value], ".2f")
    row += add_padding_center(body, header_sizes[constants.GlobalHeaders.AVERAGE_PERCENT.value])

    row += "\n"
    return row


def add_padding_center(body, header_size):
    (gap, offset) = divmod(header_size - len(body), 2)
    return ' ' * (gap + offset) + body + ' ' * (gap + 1)


def get_global_leader_board_headers():
    headers = ["" for _ in range(0, len(constants.GlobalHeaders))]
    headers[constants.GlobalHeaders.RANK.value] = "R  |"
    headers[constants.GlobalHeaders.NAME.value] = "Name"
    headers[constants.GlobalHeaders.POINTS.value] = "Points"
    headers[constants.GlobalHeaders.PROBLEMS_TRIED.value] = "#Problems"
    headers[constants.GlobalHeaders.AVERAGE_PERCENT.value] = "Mean %"
    return headers


def get_global_leader_board_header_sizes(headers, board):
    header_sizes = [len(h) + 3 for h in headers]
    header_sizes[constants.GlobalHeaders.RANK.value] = len(headers[constants.GlobalHeaders.RANK.value])
    for entry in board:
        header_sizes[constants.GlobalHeaders.NAME.value] = max(header_sizes[constants.GlobalHeaders.NAME.value],
                                                               1 + len(entry[constants.GlobalLeaderboardStruct.NAME.value]))
    max_points = max([0] + [b[constants.GlobalLeaderboardStruct.POINTS.value] for b in board])
    header_sizes[constants.GlobalHeaders.POINTS.value] = max(header_sizes[constants.GlobalHeaders.POINTS.value],
                                                             1 + len(str(max_points)))
    max_problems = max(([0] + [b[constants.GlobalLeaderboardStruct.NO_PROBLEMS.value] for b in board]))
    header_sizes[constants.GlobalHeaders.PROBLEMS_TRIED.value] = max(header_sizes[constants.GlobalHeaders.PROBLEMS_TRIED.value],
                                                                     1 + len(str(max_problems)))
    return header_sizes


def create_global_header(headers, header_sizes):
    header = headers[constants.GlobalHeaders.RANK.value]
    for i in range(1, len(headers)):
        (gap, offset) = divmod(header_sizes[i] - len(headers[i]), 2)
        header += ' ' * (gap + offset) + headers[i] + ' ' * (gap + 1)
    header += "\n" + '-' * len(header) + "\n"
    return header


def save_global_board(board):
    csv_utils.overwrite_rows(get_global_leader_board_file_name(), board)


def remove_attempt_global_leader_board(board, name, percent, points):
    user = get_user_entry_board(board, name)
    if user == get_new_global_leader_board_entry(name):
        return board
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
    user[constants.GlobalLeaderboardStruct.POINTS.value] += points
    old_total_percent = user[constants.GlobalLeaderboardStruct.AVERAGE_PERCENT.value] * user[constants.GlobalLeaderboardStruct.NO_PROBLEMS.value]
    new_total_percent = old_total_percent + percent
    new_percent = new_total_percent / (user[constants.GlobalLeaderboardStruct.NO_PROBLEMS.value] + 1.0)
    user[constants.GlobalLeaderboardStruct.AVERAGE_PERCENT.value] = new_percent
    user[constants.GlobalLeaderboardStruct.NO_PROBLEMS.value] += 1
    return user


def remove_attempt_from_user(user, percent, points):
    user[constants.GlobalLeaderboardStruct.POINTS.value] -= points
    old_total_percent = user[constants.GlobalLeaderboardStruct.AVERAGE_PERCENT.value] * user[constants.GlobalLeaderboardStruct.NO_PROBLEMS.value]
    new_total_percent = old_total_percent - percent
    user[constants.GlobalLeaderboardStruct.NO_PROBLEMS.value] -= 1
    try:
        new_percent = new_total_percent / float(user[constants.GlobalLeaderboardStruct.NO_PROBLEMS.value])
    except ZeroDivisionError:
        new_percent = 0
    user[constants.GlobalLeaderboardStruct.AVERAGE_PERCENT.value] = new_percent
    return user


def get_user_entry_board(board, name):
    entries = [b for b in board if b[constants.GlobalLeaderboardStruct.NAME.value] == name]
    if len(entries) != 0:
        return entries[0]
    else:
        return get_new_global_leader_board_entry(name)


def replace_user_entry_board(board, new_version):
    for i in range(0, len(board)):
        if board[i][constants.GlobalLeaderboardStruct.NAME.value] == new_version[constants.GlobalLeaderboardStruct.NAME.value]:
            board[i] = new_version
            return board
    # Means it's a new user
    board.append(new_version)
    return board


def get_new_global_leader_board_entry(name):
    return [name, 0, 0, 0]


# Assumes problem_id exists
def get_problem_leader_board(problem_id):
    attempts = problem_files.get_attempts(problem_id)
    return sort_problem_leader_board(attempts)


def sort_problem_leader_board(attempts):
    if len(attempts) == 0:
        return attempts
    attempts.sort(key=lambda x: -x[constants.ProblemFileStruct.PERCENT.value])
    return attempts


def sort_global_leader_board(leader_board):
    if len(leader_board) == 0:
        return leader_board
    leader_board.sort(key=lambda x: (-x[constants.GlobalLeaderboardStruct.POINTS.value], -x[constants.GlobalLeaderboardStruct.AVERAGE_PERCENT.value]))
    return leader_board


# Returns {name: points}
def calculate_points(attempts, diff):
    attempts = sort_problem_leader_board(attempts)
    filtered_attempts = remove_same_percents(attempts)
    positions = {}
    for i in range(0, len(filtered_attempts)):
        positions[filtered_attempts[i][constants.ProblemFileStruct.PERCENT.value]] = i
    result = {}
    for user in attempts:
        position_points = (len(filtered_attempts) -
                           positions[user[constants.ProblemFileStruct.PERCENT.value]])
        points = position_points * constants.DIFFICULTY_MULTIPLIER[diff]
        result[user[constants.ProblemFileStruct.NAME.value]] = points

    return result


def remove_same_percents(attempts):
    seen = set()
    result = []
    for a in attempts:
        if a[constants.ProblemFileStruct.PERCENT.value] not in seen:
            result.append(a)
            seen.add(a[constants.ProblemFileStruct.PERCENT.value])
    return result


def get_global_leader_board():
    try:
        board = csv_utils.read_csv(get_global_leader_board_file_name())
        for i in range(0, len(board)):
            board[i][constants.GlobalLeaderboardStruct.POINTS.value] = float(board[i][constants.GlobalLeaderboardStruct.POINTS.value])
            board[i][constants.GlobalLeaderboardStruct.NO_PROBLEMS.value] = int(board[i][constants.GlobalLeaderboardStruct.NO_PROBLEMS.value])
            board[i][constants.GlobalLeaderboardStruct.AVERAGE_PERCENT.value] = float(board[i][constants.GlobalLeaderboardStruct.AVERAGE_PERCENT.value])
        return board
    except FileNotFoundError:
        init.create_leaderboard()
        return get_global_leader_board()


def get_global_leader_board_file_name():
    return "data/globalLeaderboard.csv"
