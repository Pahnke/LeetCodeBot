from implements import Interface, implements
import problems_table
import problem_files
import help
import process_leaderboard
import discord_funcs
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

    def command_format(self):
        # "!command arg1, arg2"
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
@implements(CommandFace)
class Add:
    def command_title(self):
        return "!add"

    def no_args(self):
        return [3]

    def cast_arg_funcs(self):
        return [[casting_funcs.cast_difficulty,
                 casting_funcs.cast_str,
                 casting_funcs.cast_str]]

    def command_format(self):
        return "!add {difficulty}, {name}, {url}"

    async def process(self, message, args):
        # args = ["difficulty", "name", "url"]
        new_id = problems_table.get_unused_problem_id()
        # Adding it to the problem table
        problems_table.add_problem_problems_table(new_id, args[0], args[1], args[2], True)
        problem_files.create_problem_file(new_id)
        await problems_table.display_successful_problem_add(message, new_id)

    def help_message(self):
        out = "Used to add a new problem to the list of problems"
        return out


# !delete {problem ID}
@implements(CommandFace)
class Delete:
    def command_title(self):
        return "!delete"

    def no_args(self):
        return [1]

    def cast_arg_funcs(self):
        return [[casting_funcs.cast_int]]

    def command_format(self):
        return "!delete {problem ID}"

    async def process(self, message, args):
        # args = [problem ID]
        problem_id = args[0]
        if not problems_table.problem_id_exists(problem_id):
            import error_messages
            await error_messages.error_problem_does_not_exist(message, problem_id)
        # Updates score on leaderboard as well
        problem_files.delete_problem_file(problem_id)
        problems_table.remove_problem_from_problem_table(problem_id)
        await problems_table.display_successful_problem_removal(message, problem_id)

    def help_message(self):
        out = "Used to delete a problem from the list of problems."
        out += " However most of the time this command shouldn't be required"
        out += " as problems are automatically made inactive once "
        out += str(constants.NO_PLAYERS)
        out += " or more players have attempted the problem and got at least "
        out += str(constants.MIN_PERCENT)
        out += "% on it"
        return out


# !attempt {problem ID}, {better %}, {big O}, {language}
@implements(CommandFace)
class Attempt:
    def command_title(self):
        return "!attempt"

    def no_args(self):
        return [4]

    def cast_arg_funcs(self):
        return [[casting_funcs.cast_int, casting_funcs.cast_percent, casting_funcs.cast_big_o, casting_funcs.cast_str]]

    def command_format(self):
        return "!attempt {problem ID}, {better %}, {big O}, {language}"

    async def process(self, message, args):
        # args - [problem ID, better %, Big O, Language]
        problem_id = args[0]
        if not problems_table.problem_id_exists(problem_id):
            import error_messages
            await error_messages.error_problem_does_not_exist(message, problem_id)
        username = discord_funcs.get_username(message)
        # Deletes old one, updates global leaderboard as well
        await problem_files.update_attempt_to_problem_file(message, username, args[0], args[1], args[2], args[3])
        await process_leaderboard.display_problem_leader_board(message, problem_id)

    def help_message(self):
        out = "Used to submit an attempt at a problem."
        out += " Get the problem ID for a problem by typing "
        out += UserCommands.problems.value.command_title()
        return out


# !leaderboard
# !leaderboard {problem ID}
# !leaderboard -1
@implements(CommandFace)
class Leaderboard:
    def command_title(self):
        return "!leaderboard"

    def no_args(self):
        return [0, 1]

    def cast_arg_funcs(self):
        return [[], [casting_funcs.cast_int]]

    def command_format(self):
        return "!leaderboard {problem ID}?"

    async def process(self, message, args):
        # args = [(problem ID || -1)?]
        if len(args) == 0:
            await process_leaderboard.display_global_leader_board(message)
        elif args[0] == constants.ALL_ID:
            active_problem_ids = problems_table.get_active_ids()
            for problem_id in active_problem_ids:
                await process_leaderboard.display_problem_leader_board(message, problem_id)
        else:
            if not problems_table.problem_id_exists(args[0]):
                import error_messages
                await error_messages.error_problem_does_not_exist(message, args[0])
                return
            await process_leaderboard.display_problem_leader_board(message, args[0])

    def help_message(self):
        out = "Used to display one of the leaderboards."
        out += " If no argument is given then the global leaderboard is shown."
        out += " If a problem ID is given as an argument then the leaderboard for just that problem will be shown."
        out += " If the argument is {} then every problem leader board will be shown".format(constants.ALL_ID)
        return out


# !problems
# !problems {problem ID}
# !problems -1
@implements(CommandFace)
class Problems:
    def command_title(self):
        return "!problems"

    def no_args(self):
        return [0, 1]

    def cast_arg_funcs(self):
        return [[], [casting_funcs.cast_int]]

    def command_format(self):
        return "!problems {problem ID}?"

    async def process(self, message, args):
        # args = [(problem ID || -1)?]
        if len(args) == 0:
            active_problems = problems_table.get_active_problems()
            if len(active_problems) == 0:
                out = "There are currently no active problems"
                await discord_funcs.reply_to_message(message, out)
                return

            out = "Here are the active problems: "
            await discord_funcs.reply_to_message(message, out)
            for problem in active_problems:
                await problems_table.display_problem(message, problem)

        elif args[0] == constants.ALL_ID:
            all_problems = problems_table.get_all_problems()
            if len(all_problems) == 0:
                out = "There are currently no problems"
                await discord_funcs.reply_to_message(message, out)
                return

            out = "Here are all of the problems: "
            await discord_funcs.reply_to_message(message, out)
            for problem in all_problems:
                await problems_table.display_problem(message, problem)
        else:
            if not problems_table.problem_id_exists(args[0]):
                import error_messages
                await error_messages.error_problem_does_not_exist(message, args[0])
                return
            problem = problems_table.get_problem_table_problem_by_id(args[0])
            out = "Here is problem {}: ".format(args[0])
            await discord_funcs.reply_to_message(message, out)
            await problems_table.display_problem(message, problem)

    def help_message(self):
        out = "Used to display the available problems."
        out += " If no argument is given then all active problems will be shown."
        out += " If the argument is a problem ID then just that problem will be shown."
        out += " If the argument is {} then".format(constants.ALL_ID)
        out += " every problem (including inactive problems) will be shown"
        return out


# !help
# !help {command}?
@implements(CommandFace)
class Help:
    def command_title(self):
        return "!help"

    def no_args(self):
        return [0, 1]

    def cast_arg_funcs(self):
        return [[], [casting_funcs.cast_str]]

    def command_format(self):
        return "!help {command}?"

    async def process(self, message, args):
        # args = [(command)?]
        if len(args) == 0:
            await help.display_general_help(message)
        else:
            for user_command in UserCommands:
                uc_val = user_command.value
                if (args[0] == uc_val.command_title() or
                args[0] == uc_val.command_title()[1:]):
                    await help.display_help_message(message, uc_val)

    def help_message(self):
        out = "Used to learn more about commands"
        return out


class UserCommands(enum.Enum):
    add = Add()
    delete = Delete()
    attempt = Attempt()
    leaderboard = Leaderboard()
    problems = Problems()
    help = Help()
