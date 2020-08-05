import os
from pathlib import Path
import process_leaderboard
import problems_table

''' INIT FUNCS '''


def create_data_folder():
    try:
        os.mkdir("data")
    except FileExistsError:
        return


def create_problems_table():
    try:
        Path(problems_table.get_problem_table_file_name()).touch()
    except FileNotFoundError:
        create_data_folder()
        create_problems_table()
    except FileExistsError:
        return


def create_leaderboard():
    try:
        Path(process_leaderboard.get_global_leader_board_file_name()).touch()
    except FileNotFoundError:
        create_data_folder()
        create_problems_table()
    except FileExistsError:
        return


def create_attempts_folder():
    try:
        os.mkdir("data/attempts")
    except FileNotFoundError:
        create_data_folder()
        create_attempts_folder()
    except FileExistsError:
        return
