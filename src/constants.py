import enum


# Structure of stored files
class ProblemFileStruct(enum.Enum):
    NAME = 0
    PERCENT = 1
    COMPLEXITY = 2
    LANGUAGE = 3


# Forfeit values used to identify
# a forfeited attempt
# Can't manually add an attempt with percent < 0
# so FORFEIT_PERCENT uniquely identifies it
# the rest is just a "double check"
FORFEIT_PERCENT = -1
FORFEIT_BIG_O = "f"
FORFEIT_LANGUAGE = "Forfeit"


class ProblemTableStruct(enum.Enum):
    ID = 0
    NAME = 1
    DIFFICULTY = 2
    URL = 3
    ACTIVE = 4


class GlobalLeaderboardStruct(enum.Enum):
    NAME = 0
    POINTS = 1
    NO_PROBLEMS = 2
    AVERAGE_PERCENT = 3


class NameFileStruct(enum.Enum):
    DISCORD_NAME = 0
    DISPLAY_NAME = 1


class ProblemHeaders(enum.Enum):
    RANK = 0
    NAME = 1
    PERCENT = 2
    BIG_O = 3
    LANGUAGE = 4
    POINTS = 5


class GlobalHeaders(enum.Enum):
    RANK = 0
    NAME = 1
    POINTS = 2
    PROBLEMS_TRIED = 3
    AVERAGE_PERCENT = 4


# Channel name that bot responds to
CHANNEL_NAME = "leetcode"

# Select all from command
ALL_ID = -1

# Problem ID's start at 1 not 0
# It adds 1 to each found ID
FIRST_ID = 0

# Checking if active
NO_PLAYERS = 5
MIN_PERCENT = 45.0

# Maximum name length that
# is displayed in on the leaderboard
MAX_DISPLAY_NAME = 16

# The length of characters at the end
# of a username so the #1234
DISCORD_HASH_LENGTH = 5

# Maximum no chars in a message
# that discord can send
MAX_MESSAGE_SIZE = 2000

# Score calculation
DIFFICULTY_MULTIPLIER = {
    "Easy": 1.0,
    "Medium": 1.5,
    "Hard": 2.0,
}
