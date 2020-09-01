import discord_funcs
import constants

''' HELP '''


async def display_help_message(message, command):
    out = ""
    title = command.command_title()[1:]
    title = title[0].upper() + title[1:]
    out += "**" + title + ":**\n"
    out += "\t" + command.help_message() + "\n"
    if len(command.all_command_titles()) > 1:
        out += add_synonyms(command)
    out += expect_usage(command)
    await discord_funcs.reply_to_message(message, out)


# Assumes all_command_titles() > 1
def add_synonyms(command):
    out = "**Synonyms:**\n"
    out += "\tUsing "
    all_commands = ["`" + c + "`" for c in command.all_command_titles()]
    out += list_to_comma_or_str(all_commands, True)
    out += " at the start is equivalent.\n"
    return out


def list_to_comma_or_str(input_list, is_or):
    out = ""
    for i in range(0, len(input_list) - 1):
        out += str(input_list[i])
        if i + 2 < len(input_list):
            out += ", "
    if is_or:
        out += " or "
    else:
        out += " and "
    out += str(input_list[len(input_list) - 1])
    return out


async def display_general_help(message):
    import possible_commands
    out = "**LeetCodeBot**\n"
    out += "\tThis bot is designed to keep track of LeetCode problems"
    out += " and users' attempts at them."
    out += " The bot responds to messages in a channel named \"{}\"".format(constants.CHANNEL_NAME)
    out += " or via dm'ing it."
    out += " The source code for the bot can be found at: <{}>.".format(constants.SOURCE_CODE_URL)
    help_command = possible_commands.UserCommands.help.value.command_title()
    out += " Type {} followed by a command to learn more about it.\n".format(help_command)
    out += list_all_commands()
    await discord_funcs.reply_to_message(message, out)


def list_all_commands():
    import possible_commands
    out = "**Available commands:**\n"
    for command in possible_commands.UserCommands:
        out += "\t`" + command.value.command_format() + "`\n"
    return out


def expect_usage(command):
    out = "**Expected usage:**\n"
    out += "\t`" + command.command_format() + "`\n"
    return out


def explain_inactive_str():
    import config
    config_vars = config.get_config_vars()
    min_percent = config.get_var_val_from_vars(config.ConfigVars.percent.value.var_name(), config_vars)
    no_players = config.get_var_val_from_vars(config.ConfigVars.players.value.var_name(), config_vars)
    out = " A problem is inactive for everyone if {} or more players attempt".format(no_players)
    out += " (or forfeit a problem) and get above {}%.".format(min_percent)
    out += " A problem is inactive for a user if the user forfeits or attempts the problem"
    out += " and gets above {}%.".format(min_percent)
    out += " Inactive problems are hidden from standard lists to reduce clutter."
    return out
