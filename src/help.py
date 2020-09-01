import discord_funcs

''' HELP '''


async def display_help_message(message, command):
    out = ""
    title = command.command_title()[1:]
    title = title[0].upper() + title[1:]
    out += title + ": \n"
    out += "\t" + command.help_message() + "\n"
    out += expect_usage(command)
    await discord_funcs.reply_to_message(message, out)


async def display_general_help(message):
    import possible_commands
    out = ""
    help_command = possible_commands.UserCommands.help.value.command_title()
    out += "Type {} followed by a command to learn more about it\n".format(help_command)
    out += list_all_commands()
    await discord_funcs.reply_to_message(message, out)


def list_all_commands():
    import possible_commands
    out = "Available commands:\n"
    for command in possible_commands.UserCommands:
        out += "\t`" + command.value.command_format() + "`\n"
    return out


def expect_usage(command):
    out = "Expected usage:\n"
    out += "\t`" + command.command_format() + "`\n"
    return out
