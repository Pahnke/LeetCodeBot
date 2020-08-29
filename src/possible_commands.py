from implements import Interface, implements
import problems_table
import problem_files
import help
import process_leaderboard
import discord_funcs
import casting_funcs
import constants
import enum
import config

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
            return
        # Updates score on leaderboard as well
        problem_files.delete_problem_file(problem_id)
        problems_table.remove_problem_from_problem_table(problem_id)
        await problems_table.display_successful_problem_removal(message, problem_id)

    def help_message(self):
        config_vars = config.get_config_vars()
        min_percent = config.get_var_val_from_vars(config.ConfigVars.percent.value.var_name(), config_vars)
        no_players = config.get_var_val_from_vars(config.ConfigVars.players.value.var_name(), config_vars)
        out = "Used to delete a problem from the list of problems."
        out += " However most of the time this command shouldn't be required"
        out += " as problems are automatically made inactive once "
        out += str(no_players)
        out += " or more players have attempted the problem and got at least "
        out += str(min_percent)
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
            return
        # Deletes old one, updates global leaderboard as well
        await problem_files.update_attempt_to_problem_file(message, args[0], args[1], args[2], args[3])
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
            await problems_table.send_problems(message, active_problems)

        elif args[0] == constants.ALL_ID:
            all_problems = problems_table.get_all_problems()
            if len(all_problems) == 0:
                out = "There are currently no problems"
                await discord_funcs.reply_to_message(message, out)
                return

            out = "Here are all of the problems: "
            await discord_funcs.reply_to_message(message, out)
            await problems_table.send_problems(message, all_problems)
        else:
            if not problems_table.problem_id_exists(args[0]):
                import error_messages
                await error_messages.error_problem_does_not_exist(message, args[0])
                return
            problem = problems_table.get_problem_table_problem_by_id(args[0])
            out = "Here is problem {}: ".format(args[0])
            await discord_funcs.reply_to_message(message, out)
            await problems_table.send_problem(message, problem)

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
            command_name = args[0]
            for user_command in UserCommands:
                uc_val = user_command.value
                if (command_name == uc_val.command_title() or
                        command_name == uc_val.command_title()[1:]):
                    await help.display_help_message(message, uc_val)
            for var in config.ConfigVars:
                if command_name == var.value.var_name():
                    out = config.var_to_help_str(var.value, config.get_config_vars())
                    await discord_funcs.reply_to_message(message, out)

    def help_message(self):
        out = "Used to learn more about commands or config variables."
        return out


# !rename {display name}?
@implements(CommandFace)
class Rename:
    def command_title(self):
        return "!rename"

    def no_args(self):
        return [0, 1]

    def cast_arg_funcs(self):
        return [[], [casting_funcs.cast_display_name]]

    def command_format(self):
        return "!rename {display name}?"

    async def process(self, message, args):
        # args = [(display name)?]
        if len(args) == 1:
            new_name = args[0]
            process_leaderboard.add_new_display_name(message, new_name)
            await process_leaderboard.display_successful_name_update(message, new_name)
        else:
            process_leaderboard.clear_display_name(message)
            await process_leaderboard.display_successful_clear_name(message)

    def help_message(self):
        out = "Used to change name displayed on leaderboard."
        out += " The maximum name length is {}.".format(constants.MAX_DISPLAY_NAME)
        out += " To remove your display name and use your default name"
        out += " use {} with no arguments.".format(UserCommands.rename.value.command_title())
        return out


# !forfeit {problem ID}
@implements(CommandFace)
class Forfeit:
    def command_title(self):
        return "!forfeit"

    def no_args(self):
        return [1]

    def cast_arg_funcs(self):
        return [[casting_funcs.cast_int]]

    def command_format(self):
        return "!forfeit {problem ID}"

    async def process(self, message, args):
        # args = [problem ID]
        problem_id = args[0]
        if not problems_table.problem_id_exists(problem_id):
            import error_messages
            await error_messages.error_problem_does_not_exist(message, problem_id)
            return
        await problem_files.forfeit_problem(message, problem_id)
        await problem_files.display_successful_forfeit(message, problem_id)

    def help_message(self):
        out = "Used to \"forfeit\" a problem so an attempt from the user isn't required"
        out += " for the problem to be made inactive."
        out += " You can still attempt a problem which you have forfeited"
        out += " and you can forfeit a problem you have already attempted."
        out += " Forfeiting a problem you have already attempted will remove"
        out += " the previous attempt."
        return out


# !config
# !config {var name}
# !config {var name}, {var value}
@implements(CommandFace)
class Config:
    def command_title(self):
        return "!config"

    def no_args(self):
        return [0, 1, 2]

    def cast_arg_funcs(self):
        return [[], [casting_funcs.cast_str], [casting_funcs.cast_str, casting_funcs.cast_str]]

    def command_format(self):
        return "!config {var name}?, {var value}?"

    async def process(self, message, args):
        # args = [(var name)?, (var value)?]
        if len(args) == 0:
            out = config.all_config_vars_str()
            await discord_funcs.reply_to_message(message, out)
        elif len(args) == 1:
            var_name = args[0]
            if not config.check_var_exists(var_name):
                import error_messages
                await error_messages.error_var_does_not_exist(message, var_name)
                return
            config_vars = config.get_config_vars()
            var_val = config.get_var_val_from_vars(var_name, config_vars)
            out = config.var_to_str(var_name, var_val)
            await discord_funcs.reply_to_message(message, out)
        elif len(args) == 2:
            var_name = args[0]
            if not config.check_var_exists(var_name):
                import error_messages
                await error_messages.error_var_does_not_exist(message, var_name)
                return
            var_val = args[1]
            config_vars = await config.set_var(message, var_name, var_val)
            if config_vars is None:
                return
            min_percent = config.get_var_val_from_vars(config.ConfigVars.percent.value.var_name(), config_vars)
            no_players = config.get_var_val_from_vars(config.ConfigVars.players.value.var_name(), config_vars)
            problems_table.update_activity_all_problems(min_percent, no_players)
            await config.display_successful_set_var(message, var_name, var_val)

    def help_message(self):
        out = "Used to display and change variable values."
        out += " With no arguments, it will display all variables and their values."
        out += " With 1 argument, it will display just that variable's value."
        out += " With 2 arguments, it will set the variable to the new value."
        out += " All variables have default values.\n"
        out += "The possible variables that can be changed are: \n"
        config_vars = config.get_config_vars()
        for var in config.ConfigVars:
            out += "\n"
            out += config.var_to_help_str(var.value, config_vars)
        return out


class UserCommands(enum.Enum):
    add = Add()
    delete = Delete()
    attempt = Attempt()
    leaderboard = Leaderboard()
    problems = Problems()
    help = Help()
    rename = Rename()
    forfeit = Forfeit()
    config = Config()
