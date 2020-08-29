import process_leaderboard
import constants
import problems_table
import csv_utils
import init
import os
import discord_funcs
from pathlib import Path

''' PROBLEM FILES '''


# data/attempts/{problemId}.csv
# [username, beats percent, complexity, language]


def get_all_attempts(problem_id):
    try:
        attempts = csv_utils.read_csv(get_problem_file_name(problem_id))
        for i in range(0, len(attempts)):
            attempts[i][constants.ProblemFileStruct.PERCENT.value] = \
                float(attempts[i][constants.ProblemFileStruct.PERCENT.value])
        return attempts
    except FileNotFoundError:
        create_problem_file(problem_id)
        return get_all_attempts(problem_id)


def get_non_forfeit_attempts(problem_id):
    all_attempts = get_all_attempts(problem_id)
    return filter_forfeits_out(all_attempts)


def filter_forfeits_out(attempts):
    non_forfeit = [a for a in attempts if not is_a_forfeit_attempt(a)]
    return non_forfeit


def is_a_forfeit_attempt(attempt):
    return attempt[constants.ProblemFileStruct.PERCENT.value] == constants.FORFEIT_PERCENT \
           and attempt[constants.ProblemFileStruct.COMPLEXITY.value] == constants.FORFEIT_BIG_O \
           and attempt[constants.ProblemFileStruct.LANGUAGE.value] == constants.FORFEIT_LANGUAGE


def create_problem_file(problem_id):
    try:
        Path(get_problem_file_name(problem_id)).touch()
    except FileNotFoundError:
        init.create_attempts_folder()
        create_problem_file(problem_id)


def delete_problem_file(problem_id):
    attempts = get_non_forfeit_attempts(problem_id)
    global_board = process_leaderboard.get_global_leader_board()
    points = process_leaderboard.calculate_points(attempts, problems_table.get_difficulty(problem_id))
    for a in attempts:
        global_board = process_leaderboard.remove_attempt_global_leader_board(global_board,
                                                                              a[constants.ProblemFileStruct.NAME.value],
                                                                              a[
                                                                                  constants.ProblemFileStruct.PERCENT.value],
                                                                              points[a[
                                                                                  constants.ProblemFileStruct.NAME.value]])
    process_leaderboard.save_global_board(global_board)

    try:
        os.remove(get_problem_file_name(problem_id))
    except FileNotFoundError:
        # Pretty confident this Error is impossible
        # as at the start of the function,
        # the file should be read from
        return


async def update_attempt_to_problem_file(message, problem_id, percent, big_o, lang):
    all_attempts = get_all_attempts(problem_id)
    # Removes any previous forfeit attempts
    name = discord_funcs.get_username(message)
    all_attempts = [a for a in all_attempts
                    if not (a[constants.ProblemFileStruct.NAME.value] == name
                            and is_a_forfeit_attempt(a))]
    attempts = [a for a in all_attempts if not is_a_forfeit_attempt(a)]
    global_board = process_leaderboard.get_global_leader_board()
    # Deletes old attempt entries as points are based off ranking
    diff = problems_table.get_difficulty(problem_id)
    old_points = process_leaderboard.calculate_points(attempts, diff)
    for a in attempts:
        global_board = process_leaderboard.remove_attempt_global_leader_board(global_board,
                                                                              a[constants.ProblemFileStruct.NAME.value],
                                                                              a[
                                                                                  constants.ProblemFileStruct.PERCENT.value],
                                                                              old_points[a[
                                                                                  constants.ProblemFileStruct.NAME.value]])
    # Deletes lasts attempt and then
    # adds new entry into attempts
    # the new attempt could be a forfeit attempt
    attempts = [a for a in attempts if a[constants.ProblemFileStruct.NAME.value] != name]
    new_attempt = create_new_attempt(name, percent, big_o, lang)
    attempts.append(new_attempt)
    # Adds back all of the attempts into the leaderboard
    new_points = process_leaderboard.calculate_points(attempts, diff)
    for a in attempts:
        if is_a_forfeit_attempt(a):
            continue
        global_board = process_leaderboard.add_attempt_global_leader_board(global_board,
                                                                           a[constants.ProblemFileStruct.NAME.value],
                                                                           a[constants.ProblemFileStruct.PERCENT.value],
                                                                           new_points[a[
                                                                               constants.ProblemFileStruct.NAME.value]])

    process_leaderboard.save_global_board(global_board)
    # all_attempts include the correct forfeit attempts but incorrect actual attempts
    # attempts doesn't include forfeit attempts but correct actual attempts
    attempts = attempts + [a for a in all_attempts if is_a_forfeit_attempt(a)]
    save_problem_file(attempts, problem_id)
    await problems_table.update_active_val(message, attempts, problem_id)


def create_new_attempt(name, percent, big_o, lang):
    new_attempt = ["" for _ in range(0, len(constants.ProblemFileStruct))]
    new_attempt[constants.ProblemFileStruct.NAME.value] = name
    new_attempt[constants.ProblemFileStruct.PERCENT.value] = percent
    new_attempt[constants.ProblemFileStruct.COMPLEXITY.value] = big_o
    new_attempt[constants.ProblemFileStruct.LANGUAGE.value] = lang
    return new_attempt


async def forfeit_problem(message, problem_id):
    await update_attempt_to_problem_file(message, problem_id,
                                         constants.FORFEIT_PERCENT,
                                         constants.FORFEIT_BIG_O,
                                         constants.FORFEIT_LANGUAGE)


# Currently not used, but this is essentially what forfeiting is
# It's attempting a problem but with a forfeit entry
def create_new_forfeit_entry(name):
    return create_new_attempt(name,
                              constants.FORFEIT_PERCENT,
                              constants.FORFEIT_BIG_O,
                              constants.FORFEIT_LANGUAGE)


async def display_successful_forfeit(message, problem_id):
    out = "Successfully forfeited problem {} for ".format(problem_id)
    out += process_leaderboard.get_display_name(process_leaderboard.get_display_names(),
                                                discord_funcs.get_username(message))
    await discord_funcs.reply_to_message(message, out)


def save_problem_file(attempts, problem_id):
    csv_utils.overwrite_rows(get_problem_file_name(problem_id), attempts)


def get_problem_file_name(problem_id):
    return "data/attempts/" + str(problem_id) + ".csv"
