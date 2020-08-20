import csv_utils
import init
import constants
import discord_funcs

''' PROBLEMS TABLE '''
# data/problems.csv
# [id, name, difficulty, url, active]

def show_problem(problem):
    out = "[{}] ".format(problem[constants.ProblemTableStruct.ID.value])
    out += problem[constants.ProblemTableStruct.DIFFICULTY.value]
    out += " - "
    out += problem[constants.ProblemTableStruct.NAME.value]
    out += " - "
    out += "<" + problem[constants.ProblemTableStruct.URL.value] + ">"
    return out

def show_problems(problems):
    return "\n".join( show_problem(p) for p in problems )

async def send_problem(message, problem):
    await discord_funcs.reply_to_message(message, show_problem(problem))

async def send_problems(message, problems):
    await discord_funcs.reply_to_message(message, show_problems(problems))

async def display_successful_problem_add(message, problem_id):
    out = "Problem has successfully been added with ID: " + str(problem_id)
    await discord_funcs.reply_to_message(message, out)


async def display_successful_problem_removal(message, problem_id):
    out = "Problem {} has successfully been removed".format(problem_id)
    await discord_funcs.reply_to_message(message, out)


def save_problem_table(table):
    csv_utils.overwrite_rows(get_problem_table_file_name(), table)


async def update_active_val(message, attempts, problem_id):
    if len(attempts) < constants.NO_PLAYERS:
        return
    for a in attempts:
        if a[constants.ProblemFileStruct.PERCENT.value] < constants.MIN_PERCENT:
            return
    problems = get_problem_table()
    prob_name = ""
    for p in problems:
        if p[constants.ProblemTableStruct.ID.value] == problem_id:
            p[constants.ProblemTableStruct.ACTIVE.value] = False
            prob_name = p[constants.ProblemTableStruct.NAME.value]
    save_problem_table(problems)
    await display_problem_marked_inactive(message, problem_id, prob_name)


async def display_problem_marked_inactive(message, problem_id, name):
    out = "Problem {}: {} has now been made inactive.".format(problem_id, name)
    await discord_funcs.reply_to_message(message, out)


def add_problem_problems_table(problem_id, difficulty, name, url, active):
    new_entry = new_problem_table_entry(problem_id, difficulty, name, url, active)
    csv_utils.append_row(get_problem_table_file_name(), new_entry)


def remove_problem_from_problem_table(problem_id):
    problems = get_problem_table()
    new_problems = [p for p in problems if p[constants.ProblemTableStruct.ID.value] != problem_id]
    save_problem_table(new_problems)


def new_problem_table_entry(problem_id, difficulty, name, url, active):
    new_entry = ["" for _ in range(0, len(constants.ProblemTableStruct))]
    new_entry[constants.ProblemTableStruct.ID.value] = problem_id
    new_entry[constants.ProblemTableStruct.DIFFICULTY.value] = difficulty
    new_entry[constants.ProblemTableStruct.NAME.value] = name
    new_entry[constants.ProblemTableStruct.URL.value] = url
    new_entry[constants.ProblemTableStruct.ACTIVE.value] = active
    return new_entry


def problem_id_exists(problem_id):
    problems = get_problem_table()
    return len([p for p in problems if p[constants.ProblemTableStruct.ID.value] == problem_id]) == 1


def get_unused_problem_id():
    problems = get_problem_table()
    return max([p[constants.ProblemTableStruct.ID.value] for p in problems] + [constants.FIRST_ID]) + 1


def get_active_ids():
    problems = get_problem_table()
    return [p[constants.ProblemTableStruct.ID.value] for p in problems if p[constants.ProblemTableStruct.ACTIVE.value]]


def get_active_problems():
    problems = get_problem_table()
    return [p for p in problems if p[constants.ProblemTableStruct.ACTIVE.value] == "True"]


def get_all_problems():
    problems = get_problem_table()
    return [p for p in problems]


def get_difficulty(problem_id):
    problems = get_problem_table()
    return [p[constants.ProblemTableStruct.DIFFICULTY.value] for p in problems
            if p[constants.ProblemTableStruct.ID.value] == problem_id][0]


def get_name(problem_id):
    problems = get_problem_table()
    return [p[constants.ProblemTableStruct.NAME.value] for p in problems
            if p[constants.ProblemTableStruct.ID.value] == problem_id][0]


# Assume problem is in problem table
def get_problem_table_problem_by_id(problem_id):
    problems = get_problem_table()
    return [p for p in problems if p[constants.ProblemTableStruct.ID.value] == problem_id][0]


def get_problem_table():
    try:
        table = csv_utils.read_csv(get_problem_table_file_name())
        for i in range(0, len(table)):
            table[i][constants.ProblemTableStruct.ID.value] = int(table[i][constants.ProblemTableStruct.ID.value])
        return table
    except FileNotFoundError:
        init.create_problems_table()
        return get_problem_table()


def get_problem_table_file_name():
    return "data/problems.csv"
