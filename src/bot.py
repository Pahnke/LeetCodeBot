import discord

from command_classes import Commands
from error_messages import error_unknown
from parsing_commands import check_arg_types, split_args
from init import create_data_folder, \
    create_problems_table, \
    create_leaderboard, \
    create_attempts_folder
from constants import CHANNEL_NAME

'''
data/attempts/{problemId}.csv
[username, beats percent, complexity, language]

data/globalLeaderboard.csv
[username, points, problems tried, average percentage]

data/problems.csv
[id, name, difficulty, url, active]
'''


client = discord.Client()


def get_token(file_name):
    try:
        token_file = open(file_name, 'r')
        token = token_file.read()
    except FileNotFoundError:
        print("Token file ({}) not found".format(file_name))
        response = input("Enter different file name (leave blank to enter token): ")
        if not response:
            return input("Enter token: ")
        get_token(response)

    return token


@client.event
async def on_ready():
    try:
        create_data_folder()
        create_problems_table()
        create_leaderboard()
        create_attempts_folder()
    except Exception as exc:
        print("Error while initialising: ")
        print(str(exc))
        return
    print("Ready!")


@client.event
async def on_message(message):
    if (message.author == client.user
            or message.author.bot
            or message.channel.name != CHANNEL_NAME):
        return

    inputCommand = None
    for command in Commands:
        if message.content.startswith(command.command_title()):
            inputCommand = command

    if inputCommand is None:
        return

    try:
        args = split_args(message, inputCommand)
        if args is None:
            return
    except Exception as exc:
        error_unknown(message, exc, "splitting arguments")
        return

    try:
        args = check_arg_types(message, inputCommand, args)
        if args is None:
            return
    except Exception as exc:
        error_unknown(message, exc, "parsing arguments")

    try:
        inputCommand.process(message, args)
    except Exception as exc:
        error_unknown(message, exc, "processing " + inputCommand.command_title())

# Can replace token.txt with own default file name
client.run(get_token("../token.txt"))
