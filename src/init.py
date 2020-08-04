import os
from pathlib import Path
from process_leaderboard import get_global_leader_board_file_name
from problems_table import get_problem_table_file_name

''' INIT FUNCS '''


def create_data_folder():
    os.mkdir("data")


def create_problems_table():
    try:
        Path(get_problem_table_file_name()).touch()
    except FileNotFoundError:
        create_data_folder()
        create_problems_table()


def create_leaderboard():
    try:
        Path(get_global_leader_board_file_name()).touch()
    except FileNotFoundError:
        create_data_folder()
        create_problems_table()


def create_attempts_folder():
    try:
        os.mkdir("data/attempts")
    except FileNotFoundError:
        create_data_folder()
        create_attempts_folder()
