''' PARSING FUNCS '''


async def split_args(message, command):
    # !add diff, name, url
    # comma_args = [!add diff, name, url]
    # first_arg = [!add, diff]
    # args = [diff, name, url]

    comma_args = message.content.split(',')
    first_arg = comma_args[0].split(' ')
    args = []
    if len(first_arg) == 2:
        args.append(first_arg[1])
    args += comma_args[1:]
    args = [a.strip() for a in args]
    valid = False
    for possible_length in command.no_args():
        if len(args) == possible_length:
            valid = True
            break
    if not valid:
        import error_messages
        await error_messages.error_wrong_arg_no(message, command, args)
        return None
    return args


async def check_arg_types(message, command, args):
    cast_funcs = []
    for i in range(0, len(command.no_args())):
        if command.no_args()[i] == len(args):
            cast_funcs = command.cast_arg_funcs()[i]
            break
    import error_messages
    try:
        r = [cast_funcs[i](args[i]) for i in range(0, len(args))]
    except ValueError as e:
        await error_messages.error_wrong_arg_type(message, command, e)
        return None
    except Exception as e:
        await error_messages.error_unknown(message, e, "parsing arguments")
        return None
    return r
