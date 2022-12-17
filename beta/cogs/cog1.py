import discord, random, aiohttp, time, asyncio, psutil
from discord import SlashCommandGroup
from io import BytesIO
from PIL import Image
from discord.commands import Option
from discord.ext import commands
from discord.ext.commands import *
from discord.ext import commands
from .db import get_database
from .db import get_served

class NewBunny(discord.ui.View):
    def __init__(self, ctx, type):
        super().__init__(timeout=10)
        self.ctx = ctx
        self.type = type
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="You took too long! Disabled all the components.", view=self)
    @discord.ui.button(label="New bunny", style=discord.ButtonStyle.success, emoji="🐰")
    async def button_callback(self, button, interaction):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message("You're not the author of this command!", ephemeral=True)
        #if 
        if self.type != "Video":
            number = random.randint(1, 163)
            url = f"https://bunnies.media/poster/{number}.png"
            if self.type == "GIF":
                url = f"https://bunnies.media/gif/{number}.gif"
            if self.type != "Video":
                embed = discord.Embed(title="Here's a bunny!", color=discord.Color.random(), timestamp=discord.utils.utcnow(), url=url)
                embed.set_image(url=url)
                embed.set_footer(text=f"From https://bunnies.io ID: {number}")
        await interaction.response.edit_message(embed=embed)
class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @slash_command(description="Info about this bot")
    async def info(self, ctx):
        await ctx.defer(ephemeral=True)
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
        await ctx.respond ("This command is being worked on!", ephemeral=True)
        return
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
            await ctx.respond (f"I can't send messages in that channel ({channel.mention}), check my permissions and the permissions in that channel, theree is no other way for this message to appear", ephemeral=True)
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
    async def bunny(self, ctx, type: Option(str, "If you would it to be a video or image", choices=["GIF", "Image", "Video"]), id: Option(int, "The id of the bunny you want to see, from 1 to 163, not selecting this will make the ID random", required=False)):
        if id == None:
            number = random.randint(1, 163)
        if id != None:
            if id > 163:
                await ctx.respond ("That id is too high!", ephemeral=True)
                return
            if id < 1:
                await ctx.respond ("That id is too low!", ephemeral=True)
                return
            number = id
        await ctx.defer()
        if type == "Image":
            url = f"https://bunnies.media/poster/{number}.png"
        if type == "GIF":
            url = f"https://bunnies.media/gif/{number}.gif"
        if type != "Video":
            embed = discord.Embed(title="Here's a bunny!", color=discord.Color.random(), timestamp=discord.utils.utcnow(), url=url)
            embed.set_image(url=url)
            embed.set_footer(text=f"From https://bunnies.io ID: {number}")
        try:
            if type != "Video":
                await ctx.respond(embed=embed, view=NewBunny(ctx, type))
                return
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://bunnies.media/mp4/{number}.mp4", headers={'User-agent': 'Just getting some rabbits'}) as r:
                        hm = await r.content.read()
                        binary = BytesIO(hm)
                        file = discord.File(binary, filename="bunny.mp4")
                        await ctx.respond(f"Here's a bunny!\nID: {number}", file=file)
        except:
            await ctx.respond ("Uh oh! Something happened", ephemeral=True)
            raise
    @daily.command(description="No longer get pictures of bunnies every day")
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx):
        await ctx.respond ("This command is being worked on!", ephemeral=True)
        return
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
        await self.bot.get_guild(987916470690410496).get_channel(1035365139458834474).send(embed=embed)
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
        await self.bot.get_guild(987916470690410496).get_channel(1035365156600938516).send(embed=embed)
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
        else:
            await ctx.respond ("An unknown error occurred, please contact the developers! https://discord.gg/QQTngUM8GG", ephemeral=True)
            raise error
def setup(bot):
    bot.add_cog(Greetings(bot))