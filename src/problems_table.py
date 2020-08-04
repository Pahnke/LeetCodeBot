from csv_utils import *
from init import *
from constants import ProblemTableStruct, ProblemFileStruct, \
    NO_PLAYERS, MIN_PERCENT
from discord_funcs import *

''' PROBLEMS TABLE '''
# data/problems.csv
# [id, name, difficulty, url, active]


def display_problem(message, problem):
    out = "[" + problem[ProblemTableStruct.ID] + "] "
    out += problem[ProblemTableStruct.DIFFICULTY]
    out += " - "
    out += problem[ProblemTableStruct.NAME]
    out += " - "
    out += problem[ProblemTableStruct.URL]
    reply_to_message(message, out)


def display_successful_problem_add(message):
    out = "Problem has successfully been added!"
    reply_to_message(message, out)


def display_successful_problem_removal(message, problem_id):
    out = "Problem {} has successfully been removed".format(problem_id)
    reply_to_message(message, out)


def save_problem_table(table):
    overwrite_rows(get_problem_table_file_name(), table)


def update_active_val(attempts, problem_id):
    if len(attempts) < NO_PLAYERS:
        return
    for a in attempts:
        if a[ProblemFileStruct.PERCENT] < MIN_PERCENT:
            return
    problems = get_problem_table()
    for p in problems:
        if p[ProblemTableStruct.ID] == problem_id:
            p[ProblemTableStruct.ACTIVE] = False
    save_problem_table(problems)


def add_problem_problems_table(problem_id, difficulty, name, url, active):
    new_entry = new_problem_table_entry(problem_id, difficulty, name, url, active)
    append_row(get_problem_table_file_name(), new_entry)


def remove_problem_from_problem_table(problem_id):
    problems = get_problem_table()
    new_problems = [p for p in problems if p[ProblemTableStruct.ID] != problem_id]
    save_problem_table(new_problems)


def new_problem_table_entry(problem_id, difficulty, name, url, active):
    new_entry = ["" for _ in range(0, ProblemTableStruct)]
    new_entry[ProblemTableStruct.ID] = problem_id
    new_entry[ProblemTableStruct.DIFFICULTY] = difficulty
    new_entry[ProblemTableStruct.NAME] = name
    new_entry[ProblemTableStruct.URL] = url
    new_entry[ProblemTableStruct.ACTIVE] = active
    return new_entry


def problem_id_exists(problem_id):
    problems = get_problem_table()
    return len([p for p in problems if p[ProblemTableStruct.ID] == problem_id]) == 1


def get_unused_problem_id():
    problems = get_problem_table()
    return max([p[ProblemTableStruct.ID] for p in problems]) + 1


def get_active_ids():
    problems = get_problem_table()
    return [p[ProblemTableStruct.ID] for p in problems if p[ProblemTableStruct.ACTIVE]]


def get_active_problems():
    problems = get_problem_table()
    return [p for p in problems if p[ProblemTableStruct.ACTIVE]]


def get_all_problems():
    problems = get_problem_table()
    return [p for p in problems]


def get_difficulty(problem_id):
    problems = get_problem_table()
    return [p[ProblemTableStruct.DIFFICULTY] for p in problems
            if p[ProblemTableStruct.ID] == problem_id][0]


def get_name(problem_id):
    problems = get_problem_table()
    return [p[ProblemTableStruct.NAME] for p in problems
            if p[ProblemTableStruct.ID] == problem_id][0]


# Assume problem is in problem table
def get_problem_table_problem_by_id(problem_id):
    problems = get_problem_table()
    return [p for p in problems if p[ProblemTableStruct.ID] == problem_id][0]


def get_problem_table():
    try:
        return read_csv(get_problem_table_file_name())
    except FileNotFoundError:
        create_problems_table()
        return get_problem_table()


def get_problem_table_file_name():
    return "data/problems.csv"
