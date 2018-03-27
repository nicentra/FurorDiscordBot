import cfg
import discord
import datetime

client = discord.Client()

def is_member(message, member):
    return message.author == member

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user)
    print('------')
    for servers in client.servers:
        for channels in servers.channels:
            if channels.name == 'botspam':
                await client.send_message(channels, 'Bot online :robot:')
                break


@client.event
async def on_message(message):
    if message.author == client.user and not message.content.startswith(':thinking:'):
        return

    if message.content.startswith('$hello'):
        await client.send_message(message.channel, 'Hello! {0.author.mention}'.format(message))

    if message.content.startswith('$thinking'):
        await client.send_message(message.channel, ':thinking:')

    # # When invoked purges the whole channel history
    # if message.content.startswith('$purge'):
    #     timeOffSet = message.content.split(' ')
    #     if len(timeOffSet)==1:
    #         if message.author.top_role.name in cfg.ROLES:
    #             await client.purge_from(message.channel)
    #         else:
    #             await client.send_message(message.channel, 'Permission insufficient')
    #             await client.send_message(message.author, 'This is outrageous, it\'s unfair … I\'m more powerful than any of you. How can you be in the Guild and not be an Admin?')
    #     elif (not timeOffSet[1].isdecimal()) or float(timeOffSet[1])<1:
    #         await client.send_message(message.author, 'Please only enter valid numbers')
    #         await client.delete_message(message)
    #     else:
    #         if message.author.top_role.name in cfg.ROLES:
    #             await client.purge_from(message.channel, after=(message.timestamp - datetime.timedelta(minutes=int(timeOffSet[1]))))
    #         else:
    #             await client.send_message(message.channel, 'Permission insufficient')
    #             await client.send_message(message.author, 'This is outrageous, it\'s unfair … I\'m more powerful than any of you. How can you be in the Guild and not be an Admin?')

    # When invoked purges the whole channel history
    if message.content.startswith('$purge'):
        timeOffSet = message.content.split(' ')
        if len(timeOffSet) == 1:
            if message.author.top_role.name in cfg.ROLES:
                await client.purge_from(message.channel)
            else:
                await client.send_message(message.author, 'Permission insufficient')
                await client.delete_message(message)
        elif len(timeOffSet) < 3:
            await client.send_message(message.channel, 'Insufficient parameters')
        elif len(timeOffSet) > 3:
            await client.send_message(message.channel, 'Too many parameters')
        else:
            if timeOffSet[1] in cfg.TIME:
                if (not timeOffSet[2].isdecimal()) or float(timeOffSet[2]) < 1:
                    await client.send_message(message.author, 'Please only enter valid numbers')
                    await client.delete_message(message)
                else:
                    if message.author.top_role.name in cfg.ROLES:
                        await client.purge_from(message.channel, after=(
                                    message.timestamp - datetime.timedelta(minutes=int(timeOffSet[2]))))
                    else:
                        await client.send_message(message.author, 'Permission insufficient')
                        await client.delete_message(message)
            elif timeOffSet[1] in cfg.AMOUNT:
                if (not timeOffSet[2].isdecimal()) or float(timeOffSet[2]) < 1:
                    await client.send_message(message.author, 'Please only enter valid numbers')
                    await client.delete_message(message)
                else:
                    if message.author.top_role.name in cfg.ROLES:
                        await client.purge_from(message.channel, limit=int(timeOffSet[2]))
                    else:
                        await client.send_message(message.author, 'Permission insufficient')
                        await client.delete_message(message)
            elif timeOffSet[1] in cfg.MEMBER:
                mentions = message.mentions
                if message.author.top_role.name in cfg.ROLES:
                    await client.purge_from(message.channel, limit=20, check=(message.author == mentions[0]))
                else:
                    await client.send_message(message.author, 'Permission insufficient')
                    await client.delete_message(message)
            else:
                await client.send_message(message.author, 'Invalid parameter')
                await client.delete_message(message)

    if message.content.lower().startswith(tuple(cfg.NICK)):
        mentions = message.mentions
        if len(mentions) > 1:
            await client.send_message(message.author, 'Only include one mention for the command to work')
            await client.delete_message(message)
        elif len(mentions) == 1:
            if message.author.top_role.name in cfg.ROLES:
                nickname = message.content.split(' ', maxsplit=2)
                await client.change_nickname(mentions[0], nickname[len(nickname) - 1])
            else:
                await client.send_message(message.author,
                                          'This is outrageous, it\'s unfair … I\'m more powerful than any of you. How can you be in the Guild and not be an Admin?')
                await client.delete_message(message)
        else:
            nickname = message.content.split(' ', maxsplit=1)
            print('{} ; {}'.format(nickname[0], nickname[1]))
            await client.change_nickname(message.author, nickname[1])

    if message.content.startswith(':thinking:'):
        await client.add_reaction(message, '\N{THINKING FACE}')

    if message.content.startswith('$begone'):
        if message.author.top_role.name in cfg.ROLES:
            await client.send_message(message.channel, 'byebye, bot is sleepy')
            await client.logout()
        else:
            await client.send_message(message.channel, 'Permission insufficient')
            await client.send_message(message.author,
                                      'This is outrageous, it\'s unfair … I\'m more powerful than any of you. How can you be in the Guild and not be an Admin?')

    if message.content.startswith('$roster'):
        await client.send_message(message.author,
                                  'You can find the roster sheet here: https://docs.google.com/spreadsheets/d/1WLPTnuBK-RwwCC0EJH2UROAiPTUrTvXeBfEIPVYkj4Y/edit#gid=1256147381')
        await client.delete_message(message)


@client.event
async def on_member_join(member):
    await client.send_message(member,
                              'Welcome to my server, I hope you enjoy your stay! I\'m currently very much work in progress! For questions contact my programmer on discord under nicentra#7385')


client.run(cfg.TOKEN)
