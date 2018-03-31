import os


def write_to_log(log_dir, log_name, entry):
    log_path = '{}{}'.format(log_dir, log_name)

    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
        log = open(log_path, 'x')
    elif not os.path.isfile(log_path):
        log = open(log_path, 'x')
    else:
        log = open(log_path, 'a')

    log.write(entry)
    log.close()


ROLES = [
    "Admins",
    "Staff"
]

# Here follows aliases for commands

NICK = [
    "$nick ",
    "$nickname "
]

TIME = [
    "time",
    "minutes"
]

AMOUNT = [
    "last",
    "amount"
]

MEMBER = [
    "member",
    "person",
    "from"
]

# RAIDER_GREETING = discord.Embed()
