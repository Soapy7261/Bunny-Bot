import discord, aiohttp, random
from discord.ext import tasks
intents = discord.Intents.default()
intents.members = True
v = 0
oldb = ""
oldr = ""
vp = 0
oldbp = ""
oldrp = ""
bot = discord.Bot(intents=intents, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="with bunnies"))
bot.load_extension("cogs.cog1")
from cogs.db import get_database
@bot.slash_command(guild_ids=[989606575142481990])
async def re(ctx):
    if ctx.author.id != 513072262409355274:
        return
    await ctx.respond ("Reloadding.", ephemeral=True)
    try:
        bot.reload_extension("cogs.cog1")
        await ctx.respond ("Reloadded!", ephemeral=True)
    except Exception as e:
        await ctx.respond(f'```py\n{e}\n```', ephemeral=True)
@bot.event
async def on_ready():
    print ("ready!")
    premiumbunnies.start()
    bunnies.start()
@tasks.loop(hours=12)
async def premiumbunnies():
    dbname = get_database()
    collectionname = dbname['premiumservers']
    item_details = collectionname.find()
    global vp
    if vp == 2:
        vp = 0
    if vp == 0:
        urlp = "https://www.reddit.com/r/rabbits"
    if vp == 1:
        urlp = "https://www.reddit.com/r/bunnies"
    while True:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(urlp+"/hot.json", headers={'User-agent': 'Just getting some rabbits'}) as r:
                res = await r.json()
                number = random.randint(0, 25)
                if not res['data']['children'][number]["data"]["url"].endswith(('.jpg', '.png', '.jpeg')):
                    continue
                if len(res['data']['children'][number]["data"]["title"]) >= 256:
                    continue
                global oldbp
                global oldrp
                if oldbp == res['data']['children'][number]["data"]["url"]:
                    continue
                if oldrp == res['data']['children'][number]["data"]["url"]:
                    continue
                if urlp == "https://www.reddit.com/r/bunnies":
                    oldbp = res['data']['children'][number]["data"]["url"]
                if urlp == "https://www.reddit.com/r/rabbits":
                    oldrp = res['data']['children'][number]["data"]["url"]
                title = res['data']['children'][number]["data"]["title"]
                urli = res['data']['children'][number]["data"]["url"]
                embed = discord.Embed(title=title, color=discord.Color.random(), timestamp=discord.utils.utcnow(), url=urli)
                embed.set_image(url=urli)
                embed.set_footer(text=f"Taken from {urlp}")
                break

    for item in item_details:
        channel = bot.get_channel(item['channel'])
        try:
            await channel.send(embed=embed)
        except AttributeError:
            collectionname.delete_one({"channel": item['channel']})
        except discord.errors.Forbidden:
            collectionname.delete_one({"channel": item['channel']})
    vp += 1

@tasks.loop(hours=24)
async def bunnies():
    dbname = get_database()
    collectionname = dbname['servers']
    item_details = collectionname.find()
    global v
    if v == 2:
        v = 0
    if v == 0:
        url = "https://www.reddit.com/r/rabbits"
    if v == 1:
        url = "https://www.reddit.com/r/bunnies"
    while True:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url+"/hot.json", headers={'User-agent': 'Just getting some rabbits'}) as r:
                res = await r.json()
                number = random.randint(0, 25)
                if not res['data']['children'][number]["data"]["url"].endswith(('.jpg', '.png', '.jpeg')):
                    continue
                if len(res['data']['children'][number]["data"]["title"]) >= 256:
                    continue
                global oldb
                global oldr
                if oldb == res['data']['children'][number]["data"]["url"]:
                    continue
                if oldr == res['data']['children'][number]["data"]["url"]:
                    continue
                if url == "https://www.reddit.com/r/bunnies":
                    oldb = res['data']['children'][number]["data"]["url"]
                if url == "https://www.reddit.com/r/rabbits":
                    oldr = res['data']['children'][number]["data"]["url"]
                title = res['data']['children'][number]["data"]["title"]
                urli = res['data']['children'][number]["data"]["url"]
                embed = discord.Embed(title=title, color=discord.Color.random(), timestamp=discord.utils.utcnow(), url=urli)
                embed.set_image(url=urli)
                embed.set_footer(text=f"Taken from {url}")
                break

    for item in item_details:
        channel = bot.get_channel(item['channel'])
        try:
            await channel.send(embed=embed)
        except AttributeError:
            collectionname.delete_one({"channel": item['channel']})
        except discord.errors.Forbidden:
            collectionname.delete_one({"channel": item['channel']})
    v += 1

bot.run("BOTTOKEN")