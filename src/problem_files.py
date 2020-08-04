import os
from pathlib import Path
from init import *
from csv_utils import *
from process_leaderboard import remove_attempt_global_leader_board, \
    get_global_leader_board, save_global_board, add_attempt_global_leader_board, \
    calculate_points
from constants import ProblemFileStruct
from problems_table import get_difficulty, update_active_val

''' PROBLEM FILES '''
# data/attempts/{problemId}.csv
# [username, beats percent, complexity, language]


def get_attempts(problem_id):
    return read_csv(get_problem_file_name(problem_id))


def create_problem_file(problem_id):
    try:
        Path(get_problem_file_name(problem_id)).touch()
    except FileNotFoundError:
        create_attempts_folder()
        create_problem_file(problem_id)


def delete_problem_file(problem_id):
    attempts = get_attempts(problem_id)
    global_board = get_global_leader_board()
    points = calculate_points(attempts, get_difficulty(problem_id))
    for a in attempts:
        global_board = remove_attempt_global_leader_board(global_board,
                                           a[ProblemFileStruct.NAME],
                                           a[ProblemFileStruct.PERCENT],
                                           points[a[ProblemFileStruct.NAME]])
    save_global_board(global_board)

    try:
        os.remove(get_problem_file_name(problem_id))
    except FileNotFoundError:
        # Pretty confident this Error is impossible
        # as at the start of the function,
        # the file should be read from
        return


def update_attempt_to_problem_file(name, problem_id, percent, big_o, lang):
    attempts = get_attempts(problem_id)
    global_board = get_global_leader_board()

    # Deletes old attempt entries as points are based off ranking
    old_points = calculate_points(attempts)
    for a in attempts:
        global_board = remove_attempt_global_leader_board(global_board,
                                           a[ProblemFileStruct.NAME],
                                           a[ProblemFileStruct.PERCENT],
                                           old_points[a[ProblemFileStruct.NAME]])

    # Adds new entry into the attempts
    attempts = [a for a in attempts if a[ProblemFileStruct.NAME] != name]
    new_attempt = create_new_attempt(name, percent, big_o, lang)
    attempts.append(new_attempt)

    # Adds back all of the attempts into the leaderboard
    new_points = calculate_points(attempts, name)
    for a in attempts:
        global_board = add_attempt_global_leader_board(global_board,
                                                          a[ProblemFileStruct.NAME],
                                                          a[ProblemFileStruct.PERCENT],
                                                          new_points[a[ProblemFileStruct.NAME]])

    update_active_val(attempts, problem_id)
    save_global_board(global_board)
    save_problem_file(attempts, problem_id)


def create_new_attempt(name, percent, big_o, lang):
    new_attempt = ["" for _ in range(0, len(ProblemFileStruct))]
    new_attempt[ProblemFileStruct.NAME] = name
    new_attempt[ProblemFileStruct.PERCENT] = percent
    new_attempt[ProblemFileStruct.COMPLEXITY] = big_o
    new_attempt[ProblemFileStruct.LANGUAGE] = lang
    return new_attempt


def save_problem_file(attempts, problem_id):
    overwrite_rows(get_problem_file_name(problem_id), attempts)


def get_problem_file_name(problem_id):
    return "data/attempts" + str(problem_id) + ".csv"
