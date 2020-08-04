from interface import implements, Interface
from problem_files import *
from problems_table import *
from help import *
from process_leaderboard import *
from discord_funcs import get_username
from error_messages import error_problem_does_not_exist
from casting_funcs import *
import casting_funcs
import constants
import enum

''' COMMAND CLASSES '''


class CommandFace(Interface):
    def command_title(self):
        # "!command"
        pass
    def no_args(self):
        # [0, 1, 2]
        pass
    def cast_arg_funcs(self):
        # [[], [cast_str], [cast_str, cast_percent]]
        # If invalid type, cast_func's should throw a ValueError
        pass
    def command_args(self):
        # "arg1, arg2"
        pass
    def process(self, message, args):
        # The function wanted to be called
        # when the command is sent
        pass
    def help_message(self):
        # An explanation about what the function does
        # and how to use it
        pass


# !add {difficulty}, {name}, {url}
class Add(CommandFace):
    def command_title(self):
        return "!add"

    def no_args(self):
        return [3]

    def cast_arg_funcs(self):
        return [[cast_difficulty,
                 cast_str,
                 cast_str]]

    def command_format(self):
        return "!add {difficulty}, {name}, {url}"

    def process(self, message, args):
        # args = ["difficulty", "name", "url"]
        new_id = get_unused_problem_id()
        # Adding it to the problem table
        add_problem_problems_table(new_id, args[0], args[1], args[2], True)
        create_problem_file(new_id)
        display_successful_problem_add(message)

    def help_message(self):
        out = "Used to add a new problem to the list of problems"
        return out


# !delete {problem ID}
class Delete(CommandFace):
    def command_title(self):
        return "!delete"

    def no_args(self):
        return [1]

    def cast_arg_funcs(self):
        return [[cast_int]]

    def command_format(self):
        return "!delete {problem ID}"

    def process(self, message, args):
        # args = [problem ID]
        problem_id = args[0]
        if not problem_id_exists(problem_id):
            error_problem_does_not_exist(message, problem_id)
        # Updates score on leaderboard as well
        delete_problem_file(problem_id)
        remove_problem_from_problem_table(problem_id)
        display_successful_problem_removal(message, problem_id)

    def help_message(self):
        out = "Used to delete a problem from the list of problems."
        out += " However most of the time this command shouldn't be required"
        out += " as problems are automatically made inactive once "
        out += str(NO_PLAYERS)
        out += " or more players have attempted the problem and got at least "
        out += str(MIN_PERCENT)
        out += "% on it"
        return out


# !attempt {problem ID}, {better %}, {big O}, {language}
class Attempt(CommandFace):
    def command_title(self):
        return "!attempt"

    def no_args(self):
        return [4]

    def cast_arg_funcs(self):
        return [[cast_int, cast_percent, cast_big_o, cast_str]]

    def command_format(self):
        return "!attempt {problem ID}, {better %}, {big O}, {language}"

    def process(self, message, args):
        # args - [problem ID, better %, Big O, Language]
        problem_id = args[0]
        if not problem_id_exists(problem_id):
            error_problem_does_not_exist(message, problem_id)
        username = get_username(message)
        # Deletes old one, updates global leaderboard as well
        update_attempt_to_problem_file(username, args[0], args[1], args[2], args[3])
        display_problem_leader_board(message, problem_id)

    def help_message(self):
        out = "Used to submit an attempt at a problem."
        out += " Get the problem ID for a problem by typing "
        out += Commands.problems.command_title()
        return out


# !leaderboard
# !leaderboard {problem ID}
# !leaderboard -1
class Leaderboard(CommandFace):
    def command_title(self):
        return "!leaderboard"

    def no_args(self):
        return [0, 1]

    def cast_arg_funcs(self):
        return [[], [cast_int]]

    def command_format(self):
        return "!leaderboard {problem ID}?"

    def process(self, message, args):
        # args = [(problem ID || -1)?]
        if len(args) == 0:
            display_global_leader_board(message)
        elif args[0] == constants.ALL_ID:
            active_problem_ids = get_active_ids()
            for problem_id in active_problem_ids:
                display_problem_leader_board(message, problem_id)
        else:
            if not problem_id_exists(args[0]):
                error_problem_does_not_exist(message, args[0])
                return
            display_problem_leader_board(message, args[0])

    def help_message(self):
        out = "Used to display one of the leaderboards."
        out += " If no argument is given then the global leaderboard is shown."
        out += " If a problem ID is given as an argument then the leaderboard for just that problem will be shown."
        out += " If the argument is {} then every problem leader board will be shown".format(constants.ALL_ID)
        return out


# !problems
# !problems {problem ID}
# !problems -1
class Problems(CommandFace):
    def command_title(self):
        return "!problems"

    def no_args(self):
        return [0, 1]

    def cast_arg_funcs(self):
        return [[], [cast_int]]

    def command_format(self):
        return "!problems {problem ID}?"

    def process(self, message, args):
        # args = [(problem ID || -1)?]
        if len(args) == 0:
            active_problems = get_active_problems()
            out = "Here are the active problems: "
            reply_to_message(message, out)
            for problem in active_problems:
                display_problem(message, problem)
        elif args[0] == constants.ALL_ID:
            all_problems = get_all_problems()
            out = "Here are all of the problems: "
            reply_to_message(message, out)
            for problem in all_problems:
                display_problem(message, problem)
        else:
            if not problem_id_exists(args[0]):
                error_problem_does_not_exist(message, args[0])
                return
            problem = get_problem_table_problem_by_id(args[0])
            out = "Here is problem {}: ".format(args[0])
            reply_to_message(message, out)
            display_problem(message, problem)

    def help_message(self):
        out = "Used to display the available problems."
        out += " If no argument is given then all active problems will be shown."
        out += " If the argument is a problem ID then just that problem will be shown."
        out += " If the argument is {} then".format(constants.ALL_ID)
        out += " every problem (including inactive problems) will be shown"
        return out


# !help
# !help {command}?
class Help(CommandFace):
    def command_title(self):
        return "!help"

    def no_args(self):
        return [0, 1]

    def cast_arg_funcs(self):
        return [[], [cast_str]]

    def command_format(self):
        return "!help {command}?"

    def process(self, message, args):
        # args = [(command)?]
        if len(args) == 0:
            display_general_help(message)
        else:
            for command in Commands:
                if (args[0] == command.command_title() or
                args[0] == command.command_title()[1:]):
                    display_help_message(message, command)

    def help_message(self):
        out = "Used to learn more about commands"
        return out


class Commands(enum.Enum):
    add = Add()
    delete = Delete()
    attempt = Attempt()
    leaderboard = Leaderboard()
    problems = Problems()
    help = Help()
