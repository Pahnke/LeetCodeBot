import traceback
''' ERROR FUNCS '''


async def error_wrong_arg_no(message, command, args):
    title = command.command_title()
    out = error_top(title)
    out += "Wrong number of arguments found\n"
    out += "Expected to find "
    if len(command.no_args()) == 1:
        out += str(command.no_args()[0])
    else:
        for i in range(0, len(command.no_args()) - 1):
            out += command.no_args()[i]
            if i + 2 < len(command.no_args()):
                out += ", "
        out += "or " + str(command.no_args()[len(command.no_args()) - 1])
    out += " arguments but found: "
    out += str(len(args)) + "\n"
    import help
    out += help.expect_usage(command)
    out += error_bottom(title)
    import discord_funcs
    await discord_funcs.reply_to_message(message, out)


async def error_wrong_arg_type(message, command, exc):
    import help
    title = command.command_title()
    out = error_top(title)
    out += str(exc) + "\n"
    out += help.expect_usage(command)
    out += error_bottom(title)
    import discord_funcs
    await discord_funcs.reply_to_message(message, out)


async def error_problem_does_not_exist(message, problem_id):
    title = "Problem ID"
    out = error_top(title)
    out += "Problem with ID \"{}\" could not be found\n".format(problem_id)
    import possible_commands
    problem_command = possible_commands.UserCommands.problems.value.command_title()
    out += "Type {} for a list of active problems\n".format(problem_command)
    out += error_bottom(title)
    import discord_funcs
    await discord_funcs.reply_to_message(message, out)


# Eg. context = "parsing arguments"
async def error_unknown(message, e, context):
    title = "Unknown"
    out = error_top(title)
    out += "Non-anticipated error while " + context + ":\n"
    out += str(e) + "\n\n"
    out += "Stacktrace: \n"
    out += traceback.format_exc()
    out += error_bottom(title)
    import discord_funcs
    await discord_funcs.reply_to_message(message, out)


def error_top(title):
    return "---- ERROR: " + title + " ----\n"


def error_bottom(title):
    return "-" * len(error_top(title)) + "\n"
