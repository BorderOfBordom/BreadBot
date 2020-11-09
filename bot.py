import discord,os,random,asyncio,youtube_dl
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix = '%')

players = {}

@client.event
async def on_ready():
    print('bot online')

@client.event
async def on_member_join(ctx, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect(timeout=60.0,reconnect=True)
    
@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)
    await voice.disconnect()
    await ctx.send(f"Left {channel}")

@client.command(pass_context=True)
async def play(ctx, url):
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(player.title))

client.run(TOKEN)