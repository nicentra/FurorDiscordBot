import discord

TOKEN = 'NDI3NzIyNTEyMjY5MzEyMDAx.DZo1AA.sUlzLwKbCtMvG0x8Ddiv9xS04sU'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user)
    print(client.user.id)
    print('------')
    for servers in client.servers:
        s = servers
        break
    for channels in s.channels:
        #print(channels.name)
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

    # When invoked purges the whole channel history
    if message.content.startswith('$purge'):
        if message.author.top_role.name == 'Admin':
            await client.purge_from(message.channel)
        else:
            await client.send_message(message.channel, 'Permission insufficient')
            await client.send_message(message.author, 'This is outrageous, it\'s unfair … I\'m more powerful than any of you. How can you be in the Guild and not be an Admin?')


    if message.content.startswith('$nick'):
        mentions = message.mentions
        if len(mentions) > 1:
            await client.send_message(message.author, 'Only include one mention for the command to work')
            await client.delete_message(message)
        elif len(mentions) == 1:
            if message.author.top_role.name == 'Admin':
                nickname = message.content.split(' ')
                await client.change_nickname(mentions[0], nickname[len(nickname) - 1])
            else:
                await client.send_message(message.author,'This is outrageous, it\'s unfair … I\'m more powerful than any of you. How can you be in the Guild and not be an Admin?')
                await client.delete_message(message)
        else:
            nickname = message.content.split(' ', maxsplit=1)
            print('{} ; {}'.format(nickname[0], nickname[1]))
            await client.change_nickname(message.author, nickname[1])


    if message.content.startswith(':thinking:'):
        await client.add_reaction(message, '\N{THINKING FACE}')

    if message.content.startswith('$begone'):
        if message.author.top_role.name == 'Admin':
            await client.send_message(message.channel, 'byebye, bot is sleepy')
            await client.logout()
        else:
            await client.send_message(message.channel, 'Permission insufficient')
            await client.send_message(message.author, 'This is outrageous, it\'s unfair … I\'m more powerful than any of you. How can you be in the Guild and not be an Admin?')

    if message.content.startswith('$roster'):
        await client.send_message(message.author, 'You can find the roster sheet here: https://docs.google.com/spreadsheets/d/1WLPTnuBK-RwwCC0EJH2UROAiPTUrTvXeBfEIPVYkj4Y/edit#gid=1256147381')
        await client.delete_message(message)
@client.event
async def on_member_join(member):
    await client.send_message(member, 'Welcome to my server, I hope you enjoy your stay! I\'m currently very much work in progress! For questions contact my programmer on discord under nicentra#7385')




client.run(TOKEN)