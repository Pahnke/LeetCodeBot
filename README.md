# LeetCodeBot

A discord bot to generate competition to complete LeetCode problems

## Usage

`!add {difficulty}, {name}, {url}` - Add a new problem

`!delete {problem ID}` - Delete a problem (mostly not needed)

`!attempt {problem ID}, {better %}, {big O}, {language}` - Submit an attempt for a problem

`!leaderboard` - Global leaderboard

`!leaderboard {problem ID}` - Leaderboard for a problem

`!leaderboard -1` - Leaderboards for every problem

`!problems` - All active problems

`!problems {problem ID}` - Problem with specified problem ID

`!problems -1` - Every problem (including inactive problems)

`!help` - Displays a general help message

`!help {command}` - Displays a help message about for the command or config variable

`!rename {display name}` - Sets the user's name when displaying leaderboards to the display name

`!rename` - Clears the user's display name

`!forfeit {problem ID}` - Allows the user to forfeit a problem

`!config` - Displays all config variables and their values

`!config {var name}` - Displays the value of just that variable

`!config {var name}, {var val}` - Sets the variable to the new value
