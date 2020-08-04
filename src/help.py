from command_classes import Commands
from discord_funcs import reply_to_message

''' HELP '''


def display_help_message(message, command):
    out = ""
    title = command.command_title()[1:]
    title[0] = title[0].upper()
    out += title + ": \n"
    out += "\t" + command.help_message()
    out += expect_usage(command)
    reply_to_message(message, out)


def display_general_help(message):
    out = ""
    help_command = Commands.help.command_title()
    out += "Type {} followed by a command to learn more about it".format(help_command)
    out += "Available commands:\n"
    for command in Commands:
        out += "\t`" + command.command_format + "`\n"
    reply_to_message(message, out)


def expect_usage(command):
    out = "Expected usage:\n"
    out += "\t`" + command.command_format() + "`\n"
    return out
