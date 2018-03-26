import discord

TOKEN = 'NDI3NzIyNTEyMjY5MzEyMDAx.DZo1AA.sUlzLwKbCtMvG0x8Ddiv9xS04sU'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user)
    print(client.user.id)
    print('------')

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
        await client.purge_from(message.channel)

    if message.content.startswith('$nick'):
        nickname = message.content.split(' ', maxsplit=1)
        print('{} ; {}'.format(nickname[0], nickname[1]))
        await client.change_nickname(message.author, nickname[1])


    if message.content.startswith(':thinking:'):
        await client.add_reaction(message, '\N{THINKING FACE}')

@client.event
async def on_member_join(member):
    client.send_message(member, 'Welcome to my server, I hope you enjoy your stay! I\'m currently very much work in progress!')




client.run(TOKEN)