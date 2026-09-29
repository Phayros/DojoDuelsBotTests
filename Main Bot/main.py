import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import menus
from discord import app_commands
from tinydb import TinyDB, Query

Duelist_db = TinyDB("DuelistData.json")
User_db = TinyDB("UserData.json")
Db_Query = Query()

# Template for the User information in the database
class User_template():
    # Initiates the class with no info, but can receive the user discord id and the icon url
    def __init__(self,id="",icon_url=""):
        self.Id = id
        self.icon_url = icon_url
        self.achievements = {}
        self.Duelist = []
        self.Duelist_ids = []
        self.Cierites = {
            "MA": [0,0],
            "FR": [0,0],
            "ST": [0,0],
            "IS": [0,0],
            "GZ": [0,0],
            "CE": [0,0],
            "GM": [0,0],
            "AL": [0,0],
            "Jewels": 0,
            "Radiant": 0
        }
    # Export a dict with all the information so it can easily be inserted to the database
    def export_dict(self):
        profile = {
            "Id": str(self.Id),
            "Icon_url": self.icon_url,
            "Achievements": self.achievements,
            "Duelists": self.Duelist,
            "Duelist_ids": self.Duelist_ids,
            "Cierites": self.Cierites
        }
        return profile
    # Import the information from a dictionary, most likely from the database
    # Used to receive information from the database and edit it
    def import_dict(self, imported_dict: dict):
        try:
            self.Id = imported_dict["Id"]
            self.icon_url = imported_dict["Icon_url"]
            self.achievements = imported_dict["Achievements"]
            self.Duelist = imported_dict["Duelists"]
            self.Duelist_ids = imported_dict["Duelist_ids"]
            self.Cierites = imported_dict["Cierites"]
        except Exception as e:
            print(f'Error importing dict: {e}')
        return

# Template for the Duelist information in the database
class Duelist_template():
    # Initiates the class with no info, but can receive the duelist name, id and the duelist creator
    def __init__(self,name="",id=-1,creator=""):
        self.name = name
        self.id = id
        self.creator = creator
        self.icon = ""
        self.thread = ""
        self.information = ""
        self.gelta = 0
        self.medium = {
            "Animated": False,
            "Comic": False,
            "Written": False
        }
        self.win_loss_tie = [0,0,0]
    # Export a dict with all the information so it can easily be inserted to the database
    def export_dict(self):
        profile = {
            "Name": self.name,
            "Duelist_id": self.id,
            "Creator": self.creator,
            "Icon": self.icon,
            "Thread": self.thread,
            "Information": self.information,
            "Gelta": self.gelta,
            "Medium": self.medium,
            "Win_Loss_Tie": self.win_loss_tie
        }
        return profile
    # Import the information from a dictionary, most likely from the database
    # Used to receive information from the database and edit it
    def import_dict(self, imported_dict: dict):
        try:
            self.name = imported_dict["Name"]
            self.id = imported_dict["Duelist_id"]
            self.creator = imported_dict["Creator"]
            self.icon = imported_dict["Icon"]
            self.thread = imported_dict["Thread"]
            self.information = imported_dict["Information"]
            self.gelta = imported_dict["Gelta"]
            self.medium = imported_dict["Medium"]
            self.win_loss_tie = imported_dict["Win_Loss_Tie"]
        except Exception as e:
            print(f'Error importing dict: {e}')
        return

#template for duels information within the database.
class Duels_Template():
    def __init__(self, id="", thumbnail=""):
        self.id = id
        self.thumbnail = thumbnail
        self.duelists = []
        self.duelist_ids = []
        self.medium = ["Animated", "Comic", "Written"]
        self.duration = ["Speedbattle", "Short", "Medium", "Long"]
        self.duel_status = ["Active", "Completed", "Abandoned"]
        self.location = [
            "Navia",
            "The Viel",
            "Ruins of Somnus",
            "Valley of Raiterra",
            "Raiterra Forest",
            "Aether Ruins",
            "Blackwatch",
            "Aether 2.0",
            "Highgate Landing",
            "Magdurus Mountains",
            "Magdurus Pass",
            "Coquo Desert",
            "Bahp Town",
            "MicFortress",
            "The Dojo",
            "Lumaura Sanctuary",
            "Aegis Fields",
            "Shadow-Hold",
            "The Moche",
            "Magmus Ridge",
            "The Dead Forest",
            "Eternum Coast",
            "Kaihon",
            "Azurus",
            "Niera Pass",
            "Crystal Taiga",
            "Neira",
            "Other",
        ]
        pass

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

class MyMenu(menus.Menu):
    async def send_initial_messsage(self, ctx, channel):
        return await channel.send(f"Hello {ctx.author}")

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

    @app_commands.command(name="thread", description="create duelist thread")
    async def NewThreadDisplay(self, interaction: discord.Interaction, duelist: str, duelist_image: discord.Attachment, duelist_insignia: discord.Attachment):
        embed = discord.Embed(title=duelist, description=interaction.user) #creates embed
        embed.set_thumbnail(url=duelist_insignia)
        embed.set_image(url=duelist_image)
        
        # adds fields for all duelist data
        duelist_data = [("Owner", "Unknown"),
                        ("Wins", "0"),
                        ("Losses", "0"),
                        ("Medium", "Animated"),
                        ("Demo", "Link"),
                        ("Document", "Link"),
                        ("Current Gelta", "200"),
                        ("Duels", "2"),
                        ("Status", "Unavailable")]

        for name, value in duelist_data:
            embed.add_field(name=name, value=value)

        await interaction.response.send_message(embed=embed) #sends embed

        attachment_to_file = await duelist_image.to_file() # converts attachment to image
        channel = interaction.client.get_channel(int(1479982458681430026)) #gets unofficial-duelist channel ID

        result = await channel.create_thread(
        name=str(f"{duelist}"),
        file=attachment_to_file
        )  #creates thread within channel

        new_thread = interaction.client.get_channel(result.thread.id) #gets id of newly created channel 
        await new_thread.send(embed=embed) #sends message in thread
        

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