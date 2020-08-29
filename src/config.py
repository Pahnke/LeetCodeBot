from implements import Interface, implements
import enum
import csv_utils
import init
import constants
import discord_funcs
import casting_funcs


''' CONFIG VARIABLES'''


def get_config_file_name():
    return "data/config.csv"


def get_config_vars():
    try:
        return csv_utils.read_csv(get_config_file_name())
    except FileNotFoundError:
        init.create_config_file()
        return get_config_vars()


def get_var_val_from_vars(var_name, config_vars):
    var_sorted = [v[constants.ConfigFileStruct.VAR_VALUE.value] for v in config_vars
                  if v[constants.ConfigFileStruct.VAR_NAME.value] == var_name]
    if len(var_sorted) == 1:
        return var_sorted[0]
    default_val = [v.default_value() for v in ConfigVars if v.value.var_name() == var_name]
    return default_val[0]


# Assumes var_name exists
async def set_var(message, var_name, var_val_str):
    actual_var = [v.value for v in ConfigVars if v.value.var_name() == var_name][0]
    try:
        var_val = actual_var.type_func()(var_val_str)
    except ValueError as e:
        import error_messages
        await error_messages.error_wrong_var_type(message, var_name, e)
        return None
    config_vars = get_config_vars()
    removed_old = [v for v in config_vars if v[constants.ConfigFileStruct.VAR_NAME.value] != var_name]
    removed_old.append(create_config_var_entry(var_name, var_val))
    save_config_vars(config_vars)
    return config_vars


def create_config_var_entry(var_name, var_val):
    entry = ["" for _ in range(0, len(constants.ConfigFileStruct))]
    entry[constants.ConfigFileStruct.VAR_NAME.value] = var_name
    entry[constants.ConfigFileStruct.VAR_VALUE.value] = var_val
    return entry


def save_config_vars(config_vars):
    csv_utils.overwrite_rows(get_config_file_name(), config_vars)


def var_to_str(var_name, var_val):
    return var_name + ": " + var_val


def check_var_exists(var_name):
    for var in ConfigVars:
        if var.value.var_name() == var_name:
            return True
    return False


def var_to_help_str(var, config_vars):
    out = var.var_name() + ": \n"
    out += "\t" + var.explanation() + "\n"
    out += "Current Value: "
    out += get_var_val_from_vars(var.var_name(), config_vars)
    out += "\n"
    return out


def all_config_vars_str():
    config_vars = get_config_vars()
    out = "The variables that can be changed and their values are: \n"
    for var in ConfigVars:
        var_val = get_var_val_from_vars(var.value.var_name(), config_vars)
        out += "\t" + var_to_str(var.value.var_name(), var_val) + "\n"
    return out


async def display_successful_set_var(message, var_name, var_val):
    out = "Successfully set {} to {}\n".format(var_name, var_val)
    out += "The activity of problems has been set accordingly"
    await discord_funcs.reply_to_message(message, out)


class ConfigVarFace(Interface):
    def var_name(self):
        # "var name"
        # Has to be unique
        pass

    def type_func(self):
        # cast_int, cast_float
        pass

    def default_value(self):
        # n
        pass

    def explanation(self):
        # What the var controls
        pass


@implements(ConfigVarFace)
class Player:
    def var_name(self):
        return "players"

    def type_func(self):
        return casting_funcs.cast_no_players

    def default_value(self):
        return 5

    def explanation(self):
        out = "Minimum number of players required to attempt or forfeit a problem"
        out += " for that problem to be made inactive."
        return out


@implements(ConfigVarFace)
class Percent:
    def var_name(self):
        return "percent"

    def type_func(self):
        return casting_funcs.cast_percent

    def default_value(self):
        return 45.0

    def explanation(self):
        out = "Minimum percent required by all attempts at a problem"
        out += " for the problem to be made inactive."
        out += " If a problem is forfeited, the forfeited \"attempt\" will count as"
        out += " being above the minimum percent."
        return out


class ConfigVars(enum.Enum):
    players = Player()
    percent = Percent()
