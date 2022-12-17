import discord, random, aiohttp, time, asyncio, psutil
from discord import SlashCommandGroup
from discord.commands import Option
from discord.ext import commands
from discord.ext.commands import *
from discord.ext import commands
from .db import get_database
from .db import get_served

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @slash_command(description="Info about this bot")
    async def info(self, ctx):
        await ctx.defer(ephemeral=True)
        dbname = get_served()
        collection_name= dbname['served']
        item_details = collection_name.find()
        for ite in item_details:
            #global served
            served = ite['count']
        show = True
        start = time.perf_counter()
        try:
            msg = await ctx.send ("Calculating ping..")
        except:
            show = False
        if show == True:
            end = time.perf_counter()
            await msg.delete()
            duration = (end - start) * 1000
        embed = discord.Embed(title="Info about this bot", timestamp=discord.utils.utcnow(), color=0xffcb00)
        embed.add_field (name= "__Commands__", value="</bunny:1013092813195456595> </info:1013092813195456593>\n</daily set:1015699562930905139>\n</daily remove:1015699562930905139>")
        embed.add_field (name="__Support server__", value="https://discord.gg/QQTngUM8GG")
        embed.add_field (name="__Server Count__", value=len(self.bot.guilds))
        embed.add_field (name="__Bunnies Served__", value=served)
        embed.add_field (name="__Invite__", value="Click on my profile!")
        embed.add_field (name="__Users I can see__", value=len(self.bot.users))
        #embed.add_field (name="__CPU Usage__", value = f'{psutil.cpu_percent()}%')
        #embed.add_field (name="__RAM Usage__", value = f'{psutil.virtual_memory().percent}%')
        embed.add_field (name="__Websocket Ping__", value=f"{round(self.bot.latency * 1000, 2)}ms")
        if show == True:
            embed.add_field (name="__API Ping__", value=f"{round(duration, 2)}ms")
        await ctx.respond (embed=embed, ephemeral=True)
    daily = SlashCommandGroup("daily", "Daily related commands")
    @daily.command(description="Sign up for pictures of bunnies every day!")
    @commands.has_permissions(manage_channels=True)
    async def set(self, ctx, channel: Option(discord.TextChannel, "What channel you want to signup to")):
        await ctx.defer(ephemeral=True)
        if not ctx.guild:
            await ctx.respond("Please run this in a server!", ephemeral=True)
            return
        dbname = get_database()
        collectionname = dbname['servers']
        premium = dbname['premiumservers']
        item_details = collectionname.find()
        premiumname = premium.find()
        for item in premiumname:
            for x in ctx.guild.channels:
                if x.id == item['channel']:
                    await ctx.respond ("Seems this server has premium!", ephemeral=True)
                    return
        for item in item_details:
            for x in ctx.guild.channels:
                if x.id == item['channel']:
                    await ctx.respond (f"Seems your server already has a bunny messaging channel setup, if you wish to remove it, run `/daily remove`, the channel that is setup is {x.mention}", ephemeral=True)
                    return
        try:
            msg = await channel.send(".")
            await msg.delete()
        except discord.errors.Forbidden:
            await ctx.respond (f"I can't send messages in that channel ({channel.mention}), check my permissions and the permissions in that channel, there is no other way for this message to appear", ephemeral=True)
            return
        except:
            await ctx.respond ("An unknown error occurred, please contact the developers! https://discord.gg/QQTngUM8GG", ephemeral=True)
            raise
            return
        item_1 = {
            "channel": channel.id
        }
        collectionname.insert_one(item_1)
        await ctx.respond ("Added!", ephemeral=True)
    @slash_command(description="Get a picture of a bunny!")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def bunny(self, ctx):
        if ctx.guild:
            if ctx.guild.id == 987916470690410496:
                if ctx.channel.id != 1010590219906601083 and ctx.author.id != 513072262409355274:
                    await ctx.respond ("Please run this command in <#1010590219906601083>", ephemeral=True)
                    return
        await ctx.defer()
        while True:
            choice = random.randint(0, 1)
            if choice == 0:
                url = "https://www.reddit.com/r/rabbits"
            if choice == 1:
                url = "https://www.reddit.com/r/bunnies"
            async with aiohttp.ClientSession() as cs:
                    async with cs.get(url+"/hot.json", headers={'User-agent': 'Just getting some rabbits'}) as r:
                        res = await r.json()
                        try:
                            if res["error"] == 429:
                                await ctx.respond ("Seems something went wrong, trying again.")
                                await asyncio.sleep(5)
                                continue
                        except:
                            number = random.randint(1, 25)
                            if not res['data']['children'][number]["data"]["url"].endswith(('.jpg', '.png', '.jpeg')):
                                continue
                            if len(res['data']['children'][number]["data"]["title"]) >= 256:
                                continue
                            title = res['data']['children'][number]["data"]["title"]
                            urli = res['data']['children'][number]["data"]["url"]
                            embed = discord.Embed(title=title, color=discord.Color.random(), timestamp=discord.utils.utcnow(), url=urli)
                            embed.set_image(url=urli)
                            dbname = get_served()
                            collection_name = dbname["served"]
                            item_details = collection_name.find()
                            for ite in item_details:
                                global servedb
                                servedb = ite['count']+1
                                item2 = {
                                    "count": ite['count'] + 1,
                                }
                                collection_name.replace_one(ite, item2)
                            embed.set_footer(text=f"From {url}, this is the {servedb}th bunny served!")
                            try:
                                await ctx.respond(embed=embed)
                            except:
                                raise
                            break
    @daily.command(description="No longer get pictures of bunnies every day :(")
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx):
        await ctx.defer(ephemeral=True)
        if not ctx.guild:
            await ctx.respond("Please run this in a server!", ephemeral=True)
            return
        dbname = get_database()
        collectionname = dbname['servers']
        item_details = collectionname.find()
        for item in item_details:
            for x in ctx.guild.channels:
                if x.id == item['channel']:
                    await ctx.respond ("Removed.", ephemeral=True)
                    collectionname.delete_one({"channel": x.id})
                    return
        await ctx.respond ("Seems you don't have a channel setup yet", ephemeral=True)
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print ("Joined!")
        total_bots = len([member for member in guild.members if member.bot == True])
        embed = discord.Embed(title="Joined a new server!", timestamp=discord.utils.utcnow(), color=discord.Color.random())
        embed.add_field (name="Server Name:", value=guild.name)
        embed.add_field (name="Server ID:", value=guild.id)
        embed.add_field (name="Server Owner:", value=str(guild.owner))
        embed.add_field (name="Server Users:", value=len(guild.members))
        embed.add_field (name="Server Humans:", value=len(guild.members)-total_bots)
        embed.add_field (name="Server Bots:", value=total_bots)
        embed.add_field (name="Current server count:", value=len(self.bot.guilds))
        try:
            embed.set_thumbnail(url=guild.icon.url)
        except:
            pass
        await self.bot.get_guild(987916470690410496).get_channel(1010703446342639637).send(embed=embed)
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print ("Left!")
        total_bots = len([member for member in guild.members if member.bot == True])
        embed = discord.Embed(title="Left a server :(", timestamp=discord.utils.utcnow(), color=discord.Color.random())
        embed.add_field (name="Server Name:", value=guild.name)
        embed.add_field (name="Server ID:", value=guild.id)
        embed.add_field (name="Server Owner:", value=str(guild.owner))
        embed.add_field (name="Server Users:", value=len(guild.members))
        embed.add_field (name="Server Humans:", value=len(guild.members)-total_bots)
        embed.add_field (name="Server Bots:", value=total_bots)
        embed.add_field (name="Current server count:", value=len(self.bot.guilds))
        try:
            embed.set_thumbnail(url=guild.icon.url)
        except:
            pass
        await self.bot.get_guild(987916470690410496).get_channel(1010703484359819274).send(embed=embed)
    @commands.Cog.listener()
    async def on_ready(self):
        print ("Ready!")
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error): 
        if isinstance(error, commands.CommandOnCooldown):
            s = "s"
            if round(error.retry_after) == 1.00:
                s = ""
            await ctx.respond(f'You are on cooldown! You can run this command in {round(error.retry_after, 2)} second{s}', ephemeral=True)
            return
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.respond ("You need the manage messages permission to run this command!", ephemeral=True)
        elif isinstance(error, discord.ext.commands.errors.AttributeError):
            await ctx.respond ("Most likely if your seeing this message, its due to you running `/daily remove` or `/daily set` command in a DM, but if its not, please contact the developers! https://discord.gg/QQTngUM8GG", ephemeral=True)
        else:
            await ctx.respond ("An unknown error occurred, please contact the developers! https://discord.gg/QQTngUM8GG", ephemeral=True)
            raise error
def setup(bot):
    bot.add_cog(Greetings(bot))