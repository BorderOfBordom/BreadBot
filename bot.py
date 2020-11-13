import discord,os,random,asyncio,random,requests,json
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from bs4 import BeautifulSoup

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

#Gives a random decimal
@client.command(pass_context=True)
async def ranNum(ctx):
    a = random.random()
    await ctx.send(a)

#Gives a pic of bread
@client.command(pass_context=True)
async def bread(ctx):
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)

    searchurl = GOOGLE_IMAGE + 'q=bread'

    response = requests.get(searchurl,headers=usr_agent)
    html = response.text

    soup = BeautifulSoup(html,'html.parser')
    results = soup.findAll('div', {'class':'rg_i'}, limit=1)

    imagelinks = []
    for result in results:
        text = result.text
        text_dict= json.loads(text)
        link = text_dict['ou']
        imagelinks.append(link)

    for imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)

    await ctx.send(file=discord.File(response))




client.run(TOKEN)
