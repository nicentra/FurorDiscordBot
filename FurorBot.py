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
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await client.send_message(message.channel, 'Hello! {0.author.mention}'.format(message))

    if message.content.startswith('$thinking'):
        await message.channel.send(':thinking:')

client.run(TOKEN)