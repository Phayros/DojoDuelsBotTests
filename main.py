import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

# Database Setup ========
from tinydb import TinyDB, Query
Duelist_db = TinyDB("DuelistData.json")
User_db = TinyDB("UserData.json")
Db_Query = Query()
# =======================

load_dotenv()
Bot_Token = os.getenv("BOT_TOKEN_2")
Test_server_id = os.getenv("TEST_SERVER_ID")

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=Test_server_id)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commandas to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')


    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('-duels'):
            await message.channel.send(f'Hi there {message.author}, did you finish your demo?')

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('You reacted')


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=Test_server_id)

@client.tree.command(name="hello", description="Say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")

@client.tree.command(name="printer", description="I will print whatever you give me!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

@client.tree.command(name="pinger", description="Ping a discord member!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(member.mention)

@client.tree.command(name="search_duelist", description="Find a duelist by name", guild=GUILD_ID)
async def search_duelist(interaction: discord.Interaction, duelist: str):
    duelist_list_response = []
    count=0
    for each in Duelist_db.all():
        if count >= 10:
            break
        if duelist.lower() in each["Name"].lower():
            duelist_list_response.append(each)
            count+=1

    # if no match is found
    if not duelist_list_response:
        await interaction.response.send_message("Duelist not found")
        return
    # if some match is found
    result_embed = discord.Embed(title=f'Search Result for "{duelist}"')
    for each in duelist_list_response:
        link = each["Thread"] if each["Thread"] else "No application link"
        result_embed.add_field(name=each["Name"], value=f'{link}\nFrom {each["Creator"]}', inline=False)

    await interaction.response.send_message(embed=result_embed)

@client.tree.command(name="search_duelist_alt", description="Find a duelist by name", guild=GUILD_ID)
async def search_duelist_alt(interaction: discord.Interaction, duelist: str):
    duelist_list_response = []
    count=0
    for each in Duelist_db.all():
        if count >= 10:
            break
        if duelist.lower() in each["Name"].lower():
            duelist_list_response.append(each)
            count+=1

    # if no match is found
    if not duelist_list_response:
        await interaction.response.send_message("Duelist not found")
        return
    # if some match is found
    result_embed = discord.Embed(title=f'Search Result for "{duelist}"')
    for each in duelist_list_response:
        result_embed.add_field(name=f'[{each["Name"]}]({each["Thread"]})' if each["Thread"] else each["Name"], value=f'from {each["Creator"]}', inline=False)

    await interaction.response.send_message(embed=result_embed)


class User_template():
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

@client.tree.command(name="create_account", description="Creates an account for your discord user", guild=GUILD_ID)
async def Add_user(interaction: discord.Interaction):
    if User_db.search(Db_Query.Id == interaction.user.name):
        return_embed = discord.Embed(title=f'User {interaction.user.name} is already registered', colour=discord.Colour.red())
        await interaction.response.send_message(embed=return_embed)
    else:
        new_user = User_template(id=interaction.user.name,icon_url=interaction.user.avatar.url)
        User_db.insert(new_user.export_dict())
        return_embed = discord.Embed(title=f'User {interaction.user.name} successfully registered!', colour=discord.Colour.green())
        await interaction.response.send_message(embed=return_embed)

class Duelist_template():
    def __init__(self,name="",id=-1,creator=""):
        self.name = name
        self.id = id
        self.creator = creator
        self.icon = ""
        self.thread = ""
        self.information = ""
        self.gelta = 0
        self.medium = {
            "Animated": True,
            "Comic": True,
            "Written": False
        }
        self.win_loss_tie = [0,0,0]
    
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
    
    def import_dict(self, imported_dict: dict):
        try:
            self.name = imported_dict["Name"]
            self.id = imported_dict["Id"]
            self.creator = imported_dict["Creator"]
            self.icon = imported_dict["Icon"]
            self.thread = imported_dict["Thread"]
            self.information = imported_dict["Information"]
            self.gelta = imported_dict["Gelta"]
            self.medium = {
                "Animated": True,
                "Comic": True,
                "Written": False
            }
            self.win_loss_tie = [0,0,0]
        except Exception as e:
            print(f'Error importing dict: {e}')
        return

def update_user_by_name(user_name,user_dict,user_db,user_query):
    try:
        user_db.update(user_dict, user_query.Id == user_name)
    except Exception as e:
        print(f'Error updating user data: {e}')

def update_duelist_by_id(duelist_id,duelist_dict,duelist_db):
    try:
        duelist_db.update(duelist_dict, doc_ids=[duelist_id])
    except Exception as e:
        print(f'Error updating duelist data: {e}')

@client.tree.command(name="create_duelist", description="Creates a duelist linked to your account", guild=GUILD_ID)
async def Add_duelist(interaction: discord.Interaction, duelist_name: str):
    if not User_db.search(Db_Query.Id == interaction.user.name):
        return_embed = discord.Embed(title=f'User {interaction.user.name} is not registered', colour=discord.Colour.red())
        await interaction.response.send_message(embed=return_embed)
    else:
        if len(Duelist_db.all()) == 0:
            next_id = 1
        else:
            next_id = Duelist_db.all()[-1].doc_id + 1

        user_profile = User_template()
        duelist_owner = User_db.search(Db_Query.Id == interaction.user.name)[0]
        user_profile.import_dict(duelist_owner)

        user_profile.Duelist.append(duelist_name)
        user_profile.Duelist_ids.append(next_id)

        update_user_by_name(interaction.user.name,user_profile.export_dict(),User_db,Db_Query)

        new_duelist = Duelist_template(duelist_name,next_id,interaction.user.name)
        Duelist_db.insert(new_duelist.export_dict())

        return_embed = discord.Embed(title=f'Duelist {duelist_name} from {interaction.user.name} successfully registered!', colour=discord.Colour.green())
        await interaction.response.send_message(embed=return_embed)
    return
    


client.run(Bot_Token)