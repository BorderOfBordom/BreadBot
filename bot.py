import discord,os,random,asyncio,random,requests,json,aiohttp,io
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from bs4 import BeautifulSoup
from webserver import keep_alive


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

GOOGLE_IMAGE = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

counter = 0

SAVE_FOLDER = 'images'

client = commands.Bot(command_prefix = '%')

@client.event
async def on_ready():
    print('bot online')

@client.event
async def on_member_join(ctx, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)

#REEEEEE
@client.command(pass_context=True)
async def R(ctx):
    await ctx.send('EEE')

#Gives a random number between 1 and 100
@client.command(pass_context=True)
async def ranNum(ctx):
    a = (int) ((random.random()*100)+1)
    await ctx.send(a)

#Gives a pic of bread
@client.command(pass_context=True)
async def bread(ctx):
    global counter

    searchurl = GOOGLE_IMAGE + 'q=bread'

    # request url, without usr_agent, the permission gets denied
    response = requests.get(searchurl, headers=usr_agent)

    # find all divs where class='rg_meta'
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.findAll('img', {'class': 'rg_i Q4LuWd'})

    # gathering requested number of list of image links with data-src attribute
    # continue the loop in case query fails for non-data-src attributes
    count = 0
    links = []
    for res in results:
        try:
            link = res['data-src']
            links.append(link)
            count += 1
            if (count >= 100): break

        except KeyError:
            continue

    counter += 1
    if(counter >= 100): counter = 0

    link = links[counter]

    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'bread.png'))
    
    


keep_alive()

client.run(TOKEN)
