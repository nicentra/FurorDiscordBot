import datetime
import calendar
import os
import discord


def write_to_log(log_dir, log_name, entry):
    # now = datetime.datetime.now()
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

def raider_reminder(client):
    while 1:
        date = datetime.datetime.now()
        weekday = calendar.weekday(date.year, date.month, date.day)
        if (weekday == 2) and date.hour == 18 and date.minute == 28 and date.second == 0:
            for s in client.servers:
                if str(s) == 'FurorBotTest':
                    for c in s.channels:
                        if str(c) == 'botspam':
                            client.send_message(c, '@raiders Remember to sign up for raids')


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
