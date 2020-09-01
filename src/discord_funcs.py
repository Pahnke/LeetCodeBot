import constants

''' DISCORD FUNCS '''


def get_username(message):
    return message.author.name + "#" + message.author.discriminator


def is_a_dm(message):
    return message.guild is None


async def reply_to_message(message, reply):
    if len(reply) < constants.MAX_MESSAGE_SIZE:
        await message.channel.send(reply)
        return

    # Turn reply into a list of shorter replies
    # As reply is too long
    replies = split_reply(reply, "\n")
    for r in replies:
        await message.channel.send(r)
        pass


# Tries to split on newlines
# If still too long splits on spaces
# If still too long splits at index
def split_reply(reply, split_char):
    split = reply.split(split_char)
    result = []
    for s in split:
        if s < constants.MAX_MESSAGE_SIZE:
            result.append(s)
        elif split_char == '\n':
            result += split_reply(s, ' ')
        elif split_char == ' ':
            for i in range(0, len(s), constants.MAX_MESSAGE_SIZE):
                result.append(s[i:i+constants.MAX_MESSAGE_SIZE])
    return result
