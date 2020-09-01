import traceback

''' ERROR FUNCS '''


async def error_wrong_arg_no(message, command, args):
    title = command.command_title()
    body = "Wrong number of arguments found\n"
    body += "Expected to find "
    if len(command.no_args()) == 1:
        body += str(command.no_args()[0])
    else:
        import help
        body += help.list_to_comma_or_str(command.no_args(), True)
    body += " arguments but found: "
    body += str(len(args)) + "\n"
    import help
    body += help.expect_usage(command)
    await send_error(message, title, body)


async def error_wrong_arg_type(message, command, exc):
    import help
    title = command.command_title()
    body = str(exc) + "\n"
    body += help.expect_usage(command)
    await send_error(message, title, body)


async def error_wrong_var_type(message, var_name, e):
    import config
    title = var_name
    body = str(e) + "\n"
    body += "\n"
    for var in config.ConfigVars:
        if var.value.var_name() == var_name:
            body += config.var_to_help_str(var.value, config.get_config_vars())
            break
    await send_error(message, title, body)


async def error_problem_does_not_exist(message, problem_id):
    title = "Problem ID"
    body = "Problem with ID \"{}\" could not be found\n".format(problem_id)
    import possible_commands
    problem_command = possible_commands.UserCommands.problems.value.command_title()
    body += "Type {} for a list of active problems\n".format(problem_command)
    await send_error(message, title, body)


async def error_var_does_not_exist(message, var_name):
    import config
    title = "Var Name"
    body = "Config variable with name: {} does not exist.\n".format(var_name)
    body += "\n"
    body += config.all_config_vars_str()
    await send_error(message, title, body)


async def send_error(message, title, body):
    out = error_top(title)
    out += body
    out += error_bottom(title)
    import discord_funcs
    await discord_funcs.reply_to_message(message, out)


# Eg. context = "parsing arguments"
async def error_unknown(message, e, context):
    title = "Unknown"
    body = "Non-anticipated error while " + context + ":\n"
    body += str(e) + "\n\n"
    body += "Stacktrace: \n"
    body += traceback.format_exc()
    await send_error(message, title, body)


def error_top(title):
    return "---- ERROR: " + title + " ----\n"


def error_bottom(title):
    return "-" * len(error_top(title)) + "\n"
