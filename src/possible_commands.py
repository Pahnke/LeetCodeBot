from abc import ABC, abstractmethod
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


class CommandFace(ABC):
    def command_title(self):
        return self.all_command_titles()[0]

    @abstractmethod
    def all_command_titles(self):
        # ["!command", "!commands"]
        # Main one goes first
        pass

    def no_args(self):
        return [len(funcs) for funcs in self.cast_arg_funcs()]

    @abstractmethod
    def cast_arg_funcs(self):
        # [[], [cast_str], [cast_str, cast_percent]]
        # If invalid type, cast_func's should throw a ValueError
        pass

    @abstractmethod
    def argument_names(self):
        #arg1, arg2
        pass

    def command_format(self):
        return self.command_title() + " " + self.argument_names()

    @abstractmethod
    def process(self, message, args):
        # The function wanted to be called
        # when the command is sent
        pass

    @abstractmethod
    def help_message(self):
        # An explanation about what the function does
        # and how to use it
        pass


# !add {difficulty}, {name}, {url}
class Add(CommandFace):
    def all_command_titles(self):
        return ["!add"]

    def cast_arg_funcs(self):
        return [[casting_funcs.cast_difficulty,
                 casting_funcs.cast_str,
                 casting_funcs.cast_str]]

    def argument_names(self):
        return "{difficulty}, {name}, {url}"

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
class Delete(CommandFace):
    def all_command_titles(self):
        return ["!delete"]

    def cast_arg_funcs(self):
        return [[casting_funcs.cast_int]]

    def argument_names(self):
        return "{problem ID}"

    async def process(self, message, args):
        # args = [problem ID]
        problem_id = args[0]
        if not problems_table.problem_id_exists(problem_id):
            import error_messages
            return await error_messages.error_problem_does_not_exist(message, problem_id)
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
        out += " or more players have attempted (or forfeited) the problem and got at least "
        out += str(min_percent)
        out += "% on it"
        return out


# !attempt {problem ID}, {better %}, {big O}, {language}
class Attempt(CommandFace):
    def all_command_titles(self):
        return ["!attempt"]

    def cast_arg_funcs(self):
        return [[casting_funcs.cast_int, casting_funcs.cast_percent, casting_funcs.cast_big_o, casting_funcs.cast_str]]

    def argument_names(self):
        return "{problem ID}, {better %}, {big O}, {language}"

    async def process(self, message, args):
        # args - [problem ID, better %, Big O, Language]
        problem_id = args[0]
        if not problems_table.problem_id_exists(problem_id):
            import error_messages
            return await error_messages.error_problem_does_not_exist(message, problem_id)
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
class Leaderboard(CommandFace):
    def all_command_titles(self):
        return ["!leaderboard", "!leaderboards"]

    def cast_arg_funcs(self):
        return [[], [casting_funcs.cast_int]]

    def argument_names(self):
        return "{problem ID}?"

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
                return await error_messages.error_problem_does_not_exist(message, args[0])
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
class Problems(CommandFace):
    def all_command_titles(self):
        return ["!problems", "!problem"]

    def cast_arg_funcs(self):
        return [[], [casting_funcs.cast_int]]

    def argument_names(self):
        return "{problem ID}?"

    async def process(self, message, args):
        # args = [(problem ID || -1)?]
        if len(args) == 0:
            active_problems = problems_table.get_active_problems()
            if len(active_problems) == 0:
                return await problems_table.send_no_active_problems(message, False)
            if not discord_funcs.is_a_dm(message):
                out = "Here are the active problems: "
                await discord_funcs.reply_to_message(message, out)
                await problems_table.send_problems(message, active_problems)
            else:
                name = discord_funcs.get_username(message)
                config_vars = config.get_config_vars()
                min_percent = config.get_var_val_from_vars(config.ConfigVars.percent.value.var_name(), config_vars)
                new_problem_ids = []
                for p in active_problems:
                    problem_id = p[constants.ProblemTableStruct.ID.value]
                    attempts = problem_files.get_all_attempts(problem_id)
                    userAttempt = [a for a in attempts if a[constants.ProblemFileStruct.NAME.value] == name]
                    if len(userAttempt) == 0 or problems_table.attempt_fails(userAttempt[0], min_percent):
                        new_problem_ids.append(problem_id)
                new_active_problems = [p for p in active_problems
                                       if p[constants.ProblemTableStruct.ID.value] in new_problem_ids]
                if len(new_active_problems) == 0:
                    return await problems_table.send_no_active_problems(message, True)
                out = "Here are your active problems"
                await discord_funcs.reply_to_message(message, out)
                await problems_table.send_problems(message, new_active_problems)
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
                return await error_messages.error_problem_does_not_exist(message, args[0])
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
class Help(CommandFace):
    def all_command_titles(self):
        return ["!help"]

    def cast_arg_funcs(self):
        return [[], [casting_funcs.cast_str]]

    def argument_names(self):
        return "{command}?"

    async def process(self, message, args):
        # args = [(command)?]
        if len(args) == 0:
            await help.display_general_help(message)
        else:
            command_name = args[0]
            command_found = False
            # A variable and a command shouldn't have the same name
            # but in the case they somehow do, the user should see both help messages
            for user_command in UserCommands:
                uc_val = user_command.value
                if uc_matches_command_name(uc_val, command_name):
                    await help.display_help_message(message, uc_val)
                    command_found = True
            for var in config.ConfigVars:
                if command_name == var.value.var_name():
                    out = config.var_to_help_str(var.value, config.get_config_vars())
                    await discord_funcs.reply_to_message(message, out)
                    command_found = True
            if command_found:
                return
            out = "No command with name \"{}\" was found.\n".format(command_name)
            out += help.list_all_commands()
            await discord_funcs.reply_to_message(message, out)

    def help_message(self):
        out = "Used to learn more about commands or config variables."
        return out


# !rename {display name}?
class Rename(CommandFace):
    def all_command_titles(self):
        return ["!rename"]

    def cast_arg_funcs(self):
        return [[], [casting_funcs.cast_display_name]]

    def argument_names(self):
        return "{display name}?"

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
class Forfeit(CommandFace):
    def all_command_titles(self):
        return ["!forfeit"]

    def cast_arg_funcs(self):
        return [[casting_funcs.cast_int]]

    def argument_names(self):
        return "{problem ID}"

    async def process(self, message, args):
        # args = [problem ID]
        problem_id = args[0]
        if not problems_table.problem_id_exists(problem_id):
            import error_messages
            return await error_messages.error_problem_does_not_exist(message, problem_id)
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
class Config(CommandFace):
    def all_command_titles(self):
        return ["!config"]

    def cast_arg_funcs(self):
        return [[], [casting_funcs.cast_str], [casting_funcs.cast_str, casting_funcs.cast_str]]

    def argument_names(self):
        return "{var name}?, {var value}?"

    async def process(self, message, args):
        # args = [(var name)?, (var value)?]
        if len(args) == 0:
            out = config.all_config_vars_str()
            await discord_funcs.reply_to_message(message, out)
        elif len(args) == 1:
            var_name = args[0]
            if not config.check_var_exists(var_name):
                import error_messages
                return await error_messages.error_var_does_not_exist(message, var_name)
            config_vars = config.get_config_vars()
            var_val = config.get_var_val_from_vars(var_name, config_vars)
            out = config.var_to_str(var_name, var_val)
            await discord_funcs.reply_to_message(message, out)
        elif len(args) == 2:
            var_name = args[0]
            if not config.check_var_exists(var_name):
                import error_messages
                return await error_messages.error_var_does_not_exist(message, var_name)
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


def uc_matches_command_name(uc, command_name):
    for possible_name in uc.all_command_titles():
        if command_name == possible_name or command_name == possible_name[1:]:
            return True
    return False

