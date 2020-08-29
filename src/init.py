import os
from pathlib import Path
import process_leaderboard
import problems_table
import config

''' INIT FUNCS '''


def init_bot():
    create_data_folder()
    create_problems_table()
    create_leaderboard()
    create_attempts_folder()
    create_names_file()
    create_config_file()


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


def create_names_file():
    try:
        Path(process_leaderboard.get_names_file_file_name()).touch()
    except FileNotFoundError:
        create_data_folder()
    except FileExistsError:
        return


def create_config_file():
    try:
        Path(config.get_config_file_name()).touch()
    except FileNotFoundError:
        create_data_folder()
    except FileExistsError:
        return

