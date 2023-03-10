import discord
import gpt

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # To Limit the Channel where ChatGPT reads and answers Change ChannelID or remove completly
    if message.content.startswith('%') and str(message.channel.id) == 'ChannelID':
        answer = gpt.get_message_answer(message.author, message.content.split('%')[1], message.channel.id)
        await message.channel.send(answer)

with open('token', 'r') as f:
    token = f.read()
client.run(token)

