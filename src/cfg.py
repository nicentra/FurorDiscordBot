import datetime
import os


def write_to_log(entry):
    now = datetime.datetime.now()
    log_path = './log/log-{:04d}-{:02d}-{:02d}.txt'.format(now.year, now.month, now.day)

    if not os.path.isdir('./log/'):
        os.mkdir('./log/')
        log = open(log_path, 'x')
    elif not os.path.isfile(log_path):
        log = open(log_path, 'x')
    else:
        log = open(log_path, 'a')



    log.write(entry)
    log.close()


TOKEN = 'NDI3NzIyNTEyMjY5MzEyMDAx.DZo1AA.sUlzLwKbCtMvG0x8Ddiv9xS04sU'

purged_member = None

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
