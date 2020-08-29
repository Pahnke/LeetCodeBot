import discord
import parsing_commands
import init
import constants

'''
data/attempts/{problemId}.csv
[username, beats percent, complexity, language]
Functions dealing with this are in: problem_files.py

data/globalLeaderboard.csv
[username, points, problems tried, average percentage]
Functions dealing with this are in: process_leaderboard.py

data/problems.csv
[id, name, difficulty, url, active]
Functions dealing with this are in: problems_table.py

data/names.csv
[discord name, display name]
Functions dealing with this are in: process_leaderboard.py

data/config.csv
[var_name, var_val]
Functions dealing with this are in: config.py
'''


client = discord.Client()


def get_token(file_name):
    try:
        token_file = open(file_name, 'r')
        return token_file.read()
    except FileNotFoundError:
        print("Token file ({}) not found".format(file_name))
        response = input("Enter different file name (leave blank to enter token): ")
        if not response:
            return input("Enter token: ")
        return get_token(response)


@client.event
async def on_ready():
    try:
        init.init_bot()
    except Exception as exc:
        print("Error while initialising: ")
        print(str(exc))
        print(exc.args)
        return
    print("Ready!")


@client.event
async def on_message(message):
    # Ignores itself, bots,
    # any message in a server not name CHANNEL_NAME
    # Doesn't ignore dm's
    if (message.author == client.user
            or message.author.bot
            or (not (message.guild is None)
                and message.channel.name != constants.CHANNEL_NAME)):
        return

    import possible_commands
    inputCommand = None
    for possible_command in possible_commands.UserCommands:
        if message.content.startswith(possible_command.value.command_title()):
            inputCommand = possible_command.value

    if inputCommand is None:
        return

    import error_messages
    try:
        args = await parsing_commands.split_args(message, inputCommand)
        if args is None:
            return
    except Exception as exc:
        await error_messages.error_unknown(message, exc, "splitting arguments")
        return

    try:
        args = await parsing_commands.check_arg_types(message, inputCommand, args)
        if args is None:
            return
    except Exception as exc:
        await error_messages.error_unknown(message, exc, "parsing arguments")
        return

    try:
        await inputCommand.process(message, args)
    except Exception as exc:
        await error_messages.error_unknown(message, exc, "processing " + inputCommand.command_title())
        return

# Can replace token.txt with own default file name
client.run(get_token("../token.txt"))
