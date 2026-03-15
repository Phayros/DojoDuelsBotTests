import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()
Bot_Token = os.getenv("BOT_TOKEN")

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=1479962066201743625)
            synced = await self.tree.sync(guild=guild)
            print(f'synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1479962066201743625)



@app_commands.guild_only()
class UserGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="userprofile", description="user profile commands")

    @app_commands.command(name="profile", description="duel profile stats")
    async def UserProfileDisplay(self, interaction: discord.Interaction):
        embed = discord.Embed(title=interaction.user,description="User Profile Stats:")
        embed.set_thumbnail(url=interaction.user.avatar)
        
        overview_data = [("Gelta Count", "100"),
                ("Wins", "13"),
                ("Losses", "10"),
                ("Draws", "1"),
                ("Duelists", "1 (official) \n17 (unoffical)"),
                ("Cierites", "13"),]

        for name, value in overview_data:
            embed.add_field(name=name, value=value)

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="duelists", description="duelist profile stats")
    async def DuelistProfileDisplay(self, interaction: discord.Interaction):
        embed = discord.Embed(title=interaction.user,description="User Profile Stats:")
        embed.set_thumbnail(url=interaction.user.avatar)
        
        duelist_data = [("Official Duelists", "Ryobu \n Bhop \n Shale"), #call list from users official duelists in database in the future
                ("Official Duelists", "Kardashev \n Lambda \n Leonidas"),]
        
        for name, value in duelist_data:
            embed.add_field(name=name, value=value)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cierites", description="cierite profile stats")
    async def CieriteProfileDisplay(self, interaction: discord.Interaction):
        embed = discord.Embed(title=interaction.user,description="Cierite Profile Stats:")
        embed.set_thumbnail(url=interaction.user.avatar)

        cierite_data = [("Magical Amethyst", "Shards: 1 Gems: 1"),
                ("Fire Ruby", "Shards: 1 Gems: 1"),
                ("Shocking Topaz", "Shards: 1 Gems: 1"),
                ("Icy Sapphire", "Shards: 1 Gems: 1"),
                ("Gravity Zincite", "Shards: 1 Gems: 1"),
                ("Corrosive Emerald", "Shards: 1 Gems: 1"),
                ("Gale Malachite", "Shards: 1 Gems: 1"),
                ("Aqua Lazuli", "Shards: 1 Gems: 1"),
                ("Cierite Jewels", "1"),
                ("Radiant Cierium", "1")]
        
        for name, value in cierite_data:
            embed.add_field(name=name, value=value)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="achievements", description="unlockable achievements")
    async def AchievementProfileDisplay(self, interaction: discord.Interaction):
        embed = discord.Embed(title=interaction.user,description="Achievement List:")
        embed.set_thumbnail(url=interaction.user.avatar)
        
        achievement_data = [("Duels Champion", "Have the most Gelta out of every user in the server by the end of the season."),
                            ("On The Way", "Complete your first duel!"),
                            ("Beginners Luck", "Win 1 Duel"),
                            ("Killing Streak!", "Win 3 Duels in a row"),]
        
        for name, value in achievement_data:
            embed.add_field(name=name, value=value, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="gelta", description="current money count")
    async def GeltaProfileDisplay(self, interaction: discord.Interaction):
        embed = discord.Embed(title=interaction.user, description="Current Gelta Count:")
        embed.set_thumbnail(url=interaction.user.avatar)

        gelta_data = [("All Time Gelta", "1000"),
                      ("Ryobu:", "800"),
                      ("BHOP:", "200")]
        for name, value in gelta_data:
            embed.add_field(name=name, value=value)
        await interaction.response.send_message(embed=embed)

usergroup = UserGroup()
client.tree.add_command(usergroup, guild=GUILD_ID)

client.run(Bot_Token)