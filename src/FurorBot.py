''''

Github Release, required FurorBotToken.py not included. Please create in the src folder a file called FurorBotToken.py with the following line:
TOKEN = 'Your_OAuth_Token'

'''

import asyncio
import calendar
import datetime

import discord
from discord.ext import commands

from src import FurorBotToken
from src import cfg

description = '''Discord Bot for the Guild Furor on Tarren Mill-EU'''

bot = commands.Bot(command_prefix='$', description=description, pm_help=False)
prefix = bot.command_prefix

now = datetime.datetime.now()
log_dir = './log/'
log_name = 'log-{:04d}-{:02d}-{:02d}.txt'.format(now.year, now.month, now.day)


async def raid_signup_reminder():
    await bot.wait_until_ready()
    for s in bot.servers:
        if s.name == 'Furor':
            for c in s.channels:
                for r in s.roles:
                    if str(r) == 'raiders':
                        role_mention = r
                if c.name == 'raiders-chat':
                    channel = c
    while not bot.is_closed:
        date = datetime.datetime.now()
        weekday = calendar.weekday(date.year, date.month, date.day)
        if (weekday == 0 or weekday == 3) and date.hour == 19 and date.minute == 0:
            await bot.send_message(channel, '{} Remember to sign up for raids'.format(role_mention.mention))
            await asyncio.sleep(60)
        await asyncio.sleep(1)


async def raid_login_reminder():
    await bot.wait_until_ready()
    for s in bot.servers:
        if s.name == 'Furor':
            for c in s.channels:
                for r in s.roles:
                    if str(r) == 'raiders':
                        role_mention = r
                if c.name == 'raiders-chat':
                    channel = c
    while not bot.is_closed:
        date = datetime.datetime.now()
        weekday = calendar.weekday(date.year, date.month, date.day)
        if (weekday == 2 or weekday == 4 or weekday == 6) and date.hour == 18 and date.minute == 40:
            await bot.send_message(channel, '{} Log on your mains for raid!'.format(role_mention.mention))
            await asyncio.sleep(60)
        await asyncio.sleep(1)


async def close_player(voice, player):
    while voice.is_connected():
        if player.is_done():
            voice.disconnect()
        else:
            asyncio.sleep(10)


# @bot.command()
# async def help():
#     return

@bot.command(pass_context=True)
async def sr(ctx, content):
    # REMEMBER TO DOWNLOAD youtube_dl VIA PIP
    for v in bot.voice_clients:
        if v.is_connected():
            await v.disconnect()
            break
    author_channel = ctx.message.author.voice.voice_channel
    voice = await bot.join_voice_channel(author_channel)

    async def close_voice():
        await voice.disconnect()

    player = await voice.create_ytdl_player(content)
    player.start()
    player.volume = 0.1


@bot.command(pass_context=True)
async def about(ctx):
    await bot.send_message(ctx.message.author,
                           "I am a Discord bot written in Python3 based on the Discordpy library. My creator is "
                           "nicentra#7385 on discord or Strømbølina on Tarren Mill EU Horde and you can find my repository here:\n"
                           "https://github.com/nicentra/FurorDiscordBot\n"
                           "My job is to annoy the residents and raiders of the guild Furor from Tarren Mill EU on their Discord server and lend a hand where I can.\n"
                           "If you need to know about my commands please use {0}commands".format(prefix))
    if not ctx.message.channel.is_private:
        await bot.delete_message(ctx.message)


@bot.command(pass_context=True)
async def commands(ctx):
    message = ctx.message
    author = message.author
    if (not message.channel.is_private) and str(author.top_role) in cfg.ROLES:
        s = '```I have the following commands for you:\n\n' \
            '{0}commands : I\'ll provide you with this\n' \
            '{0}about : I\'ll tell you my life story :)\n' \
            '{0}hello : I\'ll greet you :)\n' \
            '{0}add X Y : returns the sum of X and Y\n' \
            '{0}multiply X Y : returns the product of X and Y\n' \
            '{0}echo : echo echo echo\n' \
            '{0}thinking : :thinking:\n' \
            '{0}roster : I\'ll provide you with a link to our roster sheet\n' \
            '{0}nick X : Changes your nickname to X\n\n' \
            '\tSidenote : The following commands are only available to admins\n\n' \
            '{0}nick @mention X : Changes the nick of @mention to X\n' \
            '{0}purge : Purges all messages from the invoked channel\n' \
            '{0}purge time X : Purges all messages from the last X minutes in the invoked channel\n' \
            '{0}purge amount X : Purges the last X messages in the invoked channel\n' \
            '{0}begone : Shuts the bot down, only available to admins```'.format(prefix)
        await bot.send_message(author, s)
        if not ctx.message.channel.is_private:
            await bot.delete_message(ctx.message)
    else:
        s = '```I have the following commands for you:\n\n' \
            '{0}commands : I\'ll provide you with this\n' \
            '{0}about : I\'ll tell you my life story :)\n' \
            '{0}hello : I\'ll greet you :)\n' \
            '{0}add X Y : returns the sum of X and Y\n' \
            '{0}multiply X Y : returns the product of X and Y\n' \
            '{0}echo : echo echo echo\n' \
            '{0}thinking : :thinking:\n' \
            '{0}roster : I\'ll provide you with a link to our roster sheet\n' \
            '{0}nick X : Changes your nickname to X```'.format(prefix)
        await bot.send_message(author, s)
        if not ctx.message.channel.is_private:
            await bot.delete_message(ctx.message)


@bot.command()
async def add(left: int, right: int = 0):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def multiply(left: int, right: int = 1):
    """Multiplies two numbers together."""
    await bot.say(left * right)


@bot.command()
async def echo(s: str):
    await bot.say('{}'.format(s))


@bot.command(pass_context=True)
async def hello(ctx):
    await bot.say('Hello {0.message.author.mention}!'.format(ctx))


@bot.command(pass_context=True)
async def nick(ctx):
    message = ctx.message
    mentions = message.mentions
    if len(mentions) == 0:
        split = message.content.split(' ', maxsplit=1)
        bot.change_nickname(message.author, split[1])
    elif len(mentions) == 1:
        if str(message.author.top_role) not in cfg.ROLES:
            await bot.send_message(message.author, 'Insufficient permission')
            if not ctx.message.channel.is_private:
                await bot.delete_message(message)
        else:
            split = message.content.split(' ', maxsplit=2)
            await bot.change_nickname(mentions[0], split[2])
    else:
        await bot.send_message(message.author, 'Too many mentions')
        if not ctx.message.channel.is_private:
            await bot.delete_message(message)


# @bot.command()
# async def repeat(times: int, *, content='repeating...'):
#     """Repeats a message multiple times."""
#     for i in range(times):
#         await bot.say(content)


@bot.command(pass_context=True)
async def purge(ctx, option: str = '', parameter='', from_parameter=100):
    message = ctx.message
    if str(message.author.top_role) not in cfg.ROLES:
        await bot.send_message(message.author, 'Insufficient permission')
        if not ctx.message.channel.is_private:
            await bot.delete_message(message)
    elif option == '':  # Purge everything
        await bot.purge_from(message.channel)
    elif option in cfg.TIME:  # Purge everything from X minutes ago
        if (not parameter.isdecimal()) or int(parameter) < 1:
            await bot.send_message(message.author, 'Please only enter valid numbers')
            if not ctx.message.channel.is_private:
                await bot.delete_message(message)
        else:
            await bot.purge_from(message.channel, after=(
                    message.timestamp - datetime.timedelta(minutes=int(parameter))))
    elif option in cfg.AMOUNT:  # Purge X amount of messages
        if (not parameter.isdecimal()) or int(parameter) < 1:
            await bot.send_message(message.author, 'Please only enter valid numbers')
            if not ctx.message.channel.is_private:
                await bot.delete_message(message)
        else:
            await bot.purge_from(message.channel, limit=(int(parameter) + 1))
    # elif option in cfg.MEMBER:  # Purge X messages from @mention, still not working properly aaaaaaaaaaargh, back to the drawing board <.<
    #     mentions = message.mentions
    #     if len(mentions) > 1:
    #         await bot.send_message(message.author, 'Only include one mention for the command to work')
    #         await bot.delete_message(message)
    #     else:
    #         if (not from_parameter.isdecimal()) or int(from_parameter) < 1:
    #             await bot.send_message(message.author, 'Please only enter valid numbers')
    #             await bot.delete_message(message)
    #         else:
    #             purged_member = mentions[0]
    #             del_count = 0
    #
    #             def is_from(m):
    #                 nonlocal del_count
    #                 nonlocal purged_member
    #                 if del_count < int(from_parameter) + 1:
    #                     del_count += 1
    #                     return m.author == purged_member
    #                 else:
    #                     return False
    #
    #             await bot.purge_from(message.channel, check=is_from)
    #             await bot.delete_message(message)
    else:
        await bot.send_message(message.author, 'Invalid parameter')
        if not ctx.message.channel.is_private:
            await bot.delete_message(message)


@bot.command()
async def thinking():
    await bot.say(':thinking:')


@bot.command(pass_context=True)
async def begone(ctx):
    if ctx.message.author.top_role.name in cfg.ROLES:
        await bot.say('byebye, bot is sleepy')
        await bot.logout()
    else:
        await bot.send_message(ctx.message.author, 'Permission insufficient')
        if not ctx.message.channel.is_private:
            await bot.delete_message(ctx.message)


@bot.command(pass_context=True)
async def roster(ctx):
    await bot.send_message(ctx.message.author,
                           'You can find the roster sheet here: https://docs.google.com/spreadsheets/d/1WLPTnuBK-RwwCC0EJH2UROAiPTUrTvXeBfEIPVYkj4Y/edit#gid=1256147381')
    if not ctx.message.channel.is_private:
        await bot.delete_message(ctx.message)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user)
    print('------')
    if not discord.opus.is_loaded():
        # the 'opus' library here is opus.dll on windows
        # or libopus.so on linux in the current directory
        # you should replace this with the location the
        # opus library is located in and with the proper filename.
        # note that on windows this DLL is automatically provided for you
        discord.opus.load_opus('opus')
    for servers in bot.servers:
        if servers.name == 'FurorBotTest':
            for channels in servers.channels:
                if channels.name == 'botspam':
                    await bot.send_message(channels, 'Bot online :robot:')
                    break
    bot.remove_command('help')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.channel.is_private:
        if message.author == message.channel.me:
            rec = message.channel.recipients[0]
        else:
            rec = message.channel.me
        time = message.timestamp
        cfg.write_to_log(log_dir, log_name,
                         'From {} to {} at {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}:\n{}\n\n'.format(message.author,
                                                                                                      rec, time.year,
                                                                                                      time.month,
                                                                                                      time.day,
                                                                                                      time.hour,
                                                                                                      time.minute,
                                                                                                      time.second,
                                                                                                      message.clean_content))

    if ':thinking:' in message.content.lower() and not message.channel.is_private:
        await bot.add_reaction(message, '\N{THINKING FACE}')

    if message.author == bot.user or message.channel.is_private:
        return


@bot.event
async def on_member_join(member):
    if member.server.name == 'FurorBotTest':
        await bot.send_message(member,
                               'Welcome to my server, I hope you enjoy your stay! I\'m currently very much work in progress! For questions contact my creator on discord under nicentra#7385 or use {0}about'.format(
                                   prefix))
    elif member.server.name == 'Furor':
        await bot.send_message(member,
                               '```Welcome to the Furor guild discord! Please make sure to change your nickname to your ingame character name (invoke {0}nick [YOURNAME] for this). '
                               'Additionally try {0}commands for a full list of commands. For questions contact my creator on discord under nicentra#7385 or use {0}about```'.format(
                                   prefix))


@bot.event
async def on_member_update(before, after):
    t = False
    for r in before.roles:
        if str(r) == 'raiders':
            t = True
    if not t:
        for r in after.roles:
            if str(r) == 'raiders':
                await bot.send_message(after,
                                       '```Welcome to our raiding team! We\'re happy to have you join us for all the future glory that awaits us (and all that sweet loot as well of course!)\n'
                                       'If you haven\'t already we would like you to read our rules when you have time off from slaying dragons and what not. '
                                       'You can find the guild rules here: '
                                       'http://forum.team-furor.com/t2694-guild-rules\n'
                                       'Furthermore, if you haven\'t yet, please change your discord nickname to your character nickname so we can recognize you! '
                                       '(You can do so with {0}nick YOURNEWNAME)\n'
                                       'Onwards to glory!```'.format(prefix))


bot.loop.create_task(raid_signup_reminder())
bot.loop.create_task(raid_login_reminder())
bot.run(FurorBotToken.TOKEN)
