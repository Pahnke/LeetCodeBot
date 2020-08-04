from discord_funcs import reply_to_message
from help import expect_usage
from command_classes import Commands

''' ERROR FUNCS '''


def error_wrong_arg_no(message, command, args):
    out = error_top(command.command_title)
    out += "Wrong number of arguments found\n"
    out += "Expected to find "
    if len(command.no_args()) == 1:
        out += str(command.no_args()[0])
    else:
        for i in range(0, len(command.no_args()) - 1):
            out += command.no_args()[i]
            if i + 2 < len(args):
                out += ", "
        out += "or " + str(command.no_args()[len(command.no_args()) - 1])
    out += " arguments but found: "
    out += str(len(args)) + "\n"
    out += expect_usage(command)
    out += error_bottom(command.command_title)
    reply_to_message(message, out)


def error_wrong_arg_type(message, command, exc):
    out = error_top(command.command_title)
    out += str(exc) + "\n"
    out += expect_usage(command)
    out += error_bottom(command.command_title)
    reply_to_message(message, out)


def error_problem_does_not_exist(message, problem_id):
    title = "Problem ID"
    out = error_top(title)
    out += "Problem ID {} could not be found\n".format(problem_id)
    problem_command = Commands.problems.command_title()
    out += "Type {} for a list of active problems\n".format(problem_command)
    out += error_bottom(title)
    reply_to_message(message, out)


# Eg. context = "parsing arguments"
def error_unknown(message, e, context):
    title = "Unknown"
    out = error_top(title)
    out += "Non-anticipated error while " + context + ":\n"
    out += str(e)
    out += error_bottom(title)
    reply_to_message(message, out)
    pass


def error_top(title):
    return "--- ERROR: " + title + " ---\n\n"


def error_bottom(command):
    return '-' * len(error_top(command) - 2)
