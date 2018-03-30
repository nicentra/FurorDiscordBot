import calendar
from src import cfg
import discord
from discord.ext import commands
import datetime
import asyncio

description = '''Discord Bot for the Guild Furor on Tarren Mill-EU'''

bot = commands.Bot(command_prefix='$', description=description, )

now = datetime.datetime.now()
log_dir = './log/'
log_name = 'log-{:04d}-{:02d}-{:02d}.txt'.format(now.year, now.month, now.day)


async def raider_reminder():
    await bot.wait_until_ready()
    for s in bot.servers:
        # print(str(s))
        if s.name == 'FurorBotTest':
            for c in s.channels:
                for r in s.roles:
                    if str(r) == 'raiders':
                        role_mention = r
                # print(str(c))
                if c.name == 'botspam':
                    channel = c
    while not bot.is_closed:
        date = datetime.datetime.now()
        weekday = calendar.weekday(date.year, date.month, date.day)
        if (weekday == 3 or weekday == 6) and date.hour == 19 and date.minute == 0:
            await bot.send_message(channel, '{} Remember to sign up for raids'.format(role_mention.mention))
            await asyncio.sleep(60)
        await asyncio.sleep(1)


@bot.command()
async def test(content):
    # print(content)
    # print(len(content.mentions))
    #
    # await bot.say('Yo {}'.format(content.mentions[0].mention))
    await bot.say('')


@bot.command()
async def add(left: int, right: int = 0):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def multiply(left: int, right: int = 1):
    """Adds two numbers together."""
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
            await bot.delete_message(message)
        else:
            split = message.content.split(' ', maxsplit=2)
            await bot.change_nickname(mentions[0], split[2])
    else:
        await bot.send_message(message.author, 'Too many mentions')
        await bot.delete_message(message)


@bot.command()
async def repeat(times: int, *, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)


@bot.command()
async def thinking():
    await bot.say(':thinking:')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user)
    print('------')
    for servers in bot.servers:
        for channels in servers.channels:
            if channels.name == 'botspam':
                await bot.send_message(channels, 'Bot online :robot:')
                break


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print(message.content)
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

    # if message.content.startswith('$hello'):
    #     await client.send_message(message.channel, 'Hello! {0.author.mention}'.format(message))

    if message.content.startswith('$thinking'):
        await bot.send_message(message.channel, ':thinking:')

    # Joke command, trigger when someone posts the thinking emoji and then adds the thinking emoji as a reaction to the message. Proof of concept
    if ':thinking:' in message.content.lower():
        await bot.add_reaction(message, '\N{THINKING FACE}')

    if message.author == bot.user or message.channel.is_private:
        return

    # for r in message.author.roles:
    #     print('{}  : No casting = {}  :  Casting = {}'.format(r, r == 'raiders', str(r) == 'raiders'))

    # await client.send_message(message.channel, 'Test mention {}'.format(message.author.roles[1].mention))

    # Command to purge the channel it has been invoked in, it has 3 options and is only useable by admins:
    # No option ($purge) => purges the maximum amount of messages from the invoked channel
    # $purge time X => purges all messages from the last X minutes
    # $purge amount X => purges last X messages
    # $purge member @mention X => Purges last X messages from the mentioned member (make sure to validate the mention)
    if message.content.lower().startswith('$purge'):
        message_content = message.content.split(' ')
        if len(message_content) == 1:
            if message.author.top_role.name in cfg.ROLES:
                await bot.purge_from(message.channel)
            else:
                await bot.send_message(message.author, 'Permission insufficient')
                await bot.delete_message(message)
        elif len(message_content) < 3:
            await bot.send_message(message.channel, 'Insufficient parameters')
        elif len(message_content) > 4:
            await bot.send_message(message.channel, 'Too many parameters')
        else:
            if message_content[1].lower() in cfg.TIME:
                if (not message_content[2].isdecimal()) or float(message_content[2]) < 1:
                    await bot.send_message(message.author, 'Please only enter valid numbers')
                    await bot.delete_message(message)
                else:
                    if message.author.top_role.name in cfg.ROLES:
                        await bot.purge_from(message.channel, after=(
                                message.timestamp - datetime.timedelta(minutes=int(message_content[2]))))
                    else:
                        await bot.send_message(message.author, 'Permission insufficient')
                        await bot.delete_message(message)
            elif message_content[1].lower() in cfg.AMOUNT:
                if (not message_content[2].isdecimal()) or float(message_content[2]) < 1:
                    await bot.send_message(message.author, 'Please only enter valid numbers')
                    await bot.delete_message(message)
                else:
                    if message.author.top_role.name in cfg.ROLES:
                        await bot.purge_from(message.channel, limit=(int(message_content[2]) + 1))
                    else:
                        await bot.send_message(message.author, 'Permission insufficient')
                        await bot.delete_message(message)
            elif message_content[1].lower() in cfg.MEMBER:
                mentions = message.mentions
                if len(mentions) > 1:
                    await bot.send_message(message.author, 'Only include one mention for the command to work')
                    await bot.delete_message(message)
                else:
                    if (not message_content[3].isdecimal()) or float(message_content[3]) < 1:
                        await bot.send_message(message.author, 'Please only enter valid numbers')
                        await bot.delete_message(message)
                    else:
                        if message.author.top_role.name in cfg.ROLES:
                            purged_member = mentions[0]
                            del_count = 0

                            def is_from(m):
                                nonlocal del_count
                                nonlocal purged_member
                                if del_count < int(message_content[3]) + 1:
                                    del_count += 1
                                    return m.author == purged_member
                                else:
                                    return False

                            await bot.purge_from(message.channel, check=is_from)
                            await bot.delete_message(message)
                        else:
                            await bot.send_message(message.author, 'Permission insufficient')
                            await bot.delete_message(message)
            else:
                await bot.send_message(message.author, 'Invalid parameter')
                await bot.delete_message(message)

    # Command to change your nickname or someone elses
    # Use $nick/$nickname "YourNewName" to change your nickname
    # Use $nick/$nickname @mention "NewNickname" to change @mention nickname, only useable by admins
    # if message.content.lower().startswith(tuple(cfg.NICK)):
    #     mentions = message.mentions
    #     if len(mentions) > 1:
    #         await bot.send_message(message.author, 'Only include one mention for the command to work')
    #         await bot.delete_message(message)
    #     elif len(mentions) == 1:
    #         if message.author.top_role.name in cfg.ROLES:
    #             nickname = message.content.split(' ', maxsplit=2)
    #             await bot.change_nickname(mentions[0], nickname[len(nickname) - 1])
    #         else:
    #             await bot.send_message(message.author, 'Permission insufficient')
    #             await bot.delete_message(message)
    #     else:
    #         nickname = message.content.split(' ', maxsplit=1)
    #         print('{} ; {}'.format(nickname[0], nickname[1]))
    #         await bot.change_nickname(message.author, nickname[1])

    # Joke command, trigger when someone posts the thinking emoji and then adds the thinking emoji as a reaction to the message. Proof of concept
    if ':thinking:' in message.content.lower():
        await bot.add_reaction(message, '\N{THINKING FACE}')

    # Shuts down the bot, can only be invoked by admins
    if message.content.lower().startswith('$begone'):
        if message.author.top_role.name in cfg.ROLES:
            await bot.send_message(message.channel, 'byebye, bot is sleepy')
            await bot.logout()
        else:
            await bot.send_message(message.author, 'Permission insufficient')
            await bot.delete_message(message)

    # Command which whispers the invoker the link to our roster sheet
    if message.content.lower().startswith('$roster'):
        await bot.send_message(message.author,
                               'You can find the roster sheet here: https://docs.google.com/spreadsheets/d/1WLPTnuBK-RwwCC0EJH2UROAiPTUrTvXeBfEIPVYkj4Y/edit#gid=1256147381')
        await bot.delete_message(message)


@bot.event
async def on_member_join(member):
    if member.server.name == 'FurorBotTest':
        await bot.send_message(member,
                               'Welcome to my server, I hope you enjoy your stay! I\'m currently very much work in progress! For questions contact my creator on discord under nicentra#7385')
    else:
        await bot.send_message(member,
                               'Welcome to the Furor guild discord! Please make sure to change your nickname to your ingame character name (invoke $nick [YOURNAME] for this). Additionally try $commands for a full list of commands. For questions contact my creator on discord under nicentra#7385')


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
                                       'Congratulations on becoming a part of the raid team! If you haven\'t yet, please change your server nickname to your ingame charactername so we can identify you! The easiest way to do so is using my command $nick MyNewNickname !\n\nFurthermore, be sure to check out our #resources where you can a link to our forums, our attendance sheet as well as a list of mandatory addons!')


bot.loop.create_task(raider_reminder())
bot.run(cfg.TOKEN)
