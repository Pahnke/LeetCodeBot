import enum


# Structure of stored files
class ProblemFileStruct(enum.Enum):
    NAME = 0
    PERCENT = 1
    COMPLEXITY = 2
    LANGUAGE = 3


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
NO_PLAYERS = 1
MIN_PERCENT = 45.0

# Maximum no chars in a message
# that discord can send
MAX_MESSAGE_SIZE = 2000

# Score calculation
DIFFICULTY_MULTIPLIER = {
    "Easy": 1.0,
    "Medium": 1.5,
    "Hard": 2.0,
}

