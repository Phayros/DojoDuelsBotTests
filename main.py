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

# Enviroment variables
load_dotenv()
Bot_Token = os.getenv("BOT_TOKEN_2")
Test_server_id = os.getenv("TEST_SERVER_ID")


# First tutorial stuff, I dont remember why this is here, once I make sure removing it dont break the code I'll delete it
# Class client gives the ability to use all associated bot functionality, it is instanced and contained in "client" on line 49 - Corvid
class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=Test_server_id)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commandas to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

# all 3 functions down here can be deleted without issue
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('-duels'):
            await message.channel.send(f'Hi there {message.author}, did you finish your demo?')

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('You reacted')

# ============================================================

# Intents and intial configuration for the bot to run
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

# ID of the server the bot will run
GUILD_ID = discord.Object(id=Test_server_id)

# Simple function just to reply with "Hi there!"
@client.tree.command(name="hello", description="Say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")

# Simple function just to send a message with the message the user sent in the command
@client.tree.command(name="printer", description="I will print whatever you give me!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

# Simple function that pings someone in the server
@client.tree.command(name="pinger", description="Ping a discord member!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(member.mention)

# Function to search a duelist in the database
# it compares the string sent with the names of the duelists in the database
# if the string is inside the name of the duelist it will be selected for the
# it stops at 10 to make sure the search dont get too full
# A new version with pagination will be implemented later
@client.tree.command(name="search_duelist", description="Find a duelist by name", guild=GUILD_ID)
async def search_duelist(interaction: discord.Interaction, duelist: str):
    # Initializes the list of duelists that will receive the duelists that match the search
    duelist_list_response = []
    # Count variable used to stop the loop once 10 duelists are found
    count=0
    # loop that iterates the whole database
    for each in Duelist_db.all():
        # break condition
        if count >= 10:
            break
        # Checks if the string recieved is inside the name of the duelist name checked
        # It makes both strings be lower so its not case sensitive
        if duelist.lower() in each["Name"].lower():
            # If it matches the duelist is added to the list and the count variable is incremented
            duelist_list_response.append(each)
            count+=1

    # if no match is found
    if not duelist_list_response:
        await interaction.response.send_message("Duelist not found")
        return
    # if some match is found
    # Creates an embed and iterates through the list of duelists found and to add their information to the embed
    result_embed = discord.Embed(title=f'Search Result for "{duelist}"')
    for each in duelist_list_response:
        link = each["Thread"] if each["Thread"] else "No application link"
        result_embed.add_field(name=each["Name"], value=f'{link}\nFrom {each["Creator"]}', inline=False)

    await interaction.response.send_message(embed=result_embed)

# Function to search a duelist just like the last one but used a different formatation that didn't worked

# @client.tree.command(name="search_duelist_alt", description="Find a duelist by name", guild=GUILD_ID)
# async def search_duelist_alt(interaction: discord.Interaction, duelist: str):
#     duelist_list_response = []
#     count=0
#     for each in Duelist_db.all():
#         if count >= 10:
#             break
#         if duelist.lower() in each["Name"].lower():
#             duelist_list_response.append(each)
#             count+=1

#     # if no match is found
#     if not duelist_list_response:
#         await interaction.response.send_message("Duelist not found")
#         return
#     # if some match is found
#     result_embed = discord.Embed(title=f'Search Result for "{duelist}"')
#     for each in duelist_list_response:
#         result_embed.add_field(name=f'[{each["Name"]}]({each["Thread"]})' if each["Thread"] else each["Name"], value=f'from {each["Creator"]}', inline=False)

#     await interaction.response.send_message(embed=result_embed)

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

# Function used to add a user to the database
# It adds the user that used the command
@client.tree.command(name="create_account", description="Creates an account for your discord user", guild=GUILD_ID)
async def Add_user(interaction: discord.Interaction):
    # Checks if the user is already registered and returns a message warning the user if thats the case
    if User_db.search(Db_Query.Id == interaction.user.name):
        return_embed = discord.Embed(title=f'User {interaction.user.name} is already registered', colour=discord.Colour.red())
        await interaction.response.send_message(embed=return_embed)
    # If the user is not registered a user template is created and its inserted into the database
    # A message will be sent confirming that the user was registered
    else:
        new_user = User_template(id=interaction.user.name,icon_url=interaction.user.avatar.url)
        User_db.insert(new_user.export_dict())
        return_embed = discord.Embed(title=f'User {interaction.user.name} successfully registered!', colour=discord.Colour.green())
        await interaction.response.send_message(embed=return_embed)

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

# Function used to find and update a user by searching the database from the user discord id
# This function assumes the user is in the database and doesnt check for it
def update_user_by_name(user_name,user_dict,user_db,user_query):
    try:
        user_db.update(user_dict, user_query.Id == user_name)
    except Exception as e:
        print(f'Error updating user data: {e}')

# Function used to find and update a duelist by going directly to it using the duelist id
# This function assumes the duelist is in the database and will not check for it
def update_duelist_by_id(duelist_id,duelist_dict,duelist_db):
    try:
        duelist_db.update(duelist_dict, doc_ids=[duelist_id])
    except Exception as e:
        print(f'Error updating duelist data: {e}')

# Function used to create and insert a duelist into the database
# The user must be registered in the system and the duelist will be linked to the user that created it
@client.tree.command(name="create_duelist", description="Creates a duelist linked to your account", guild=GUILD_ID)
async def Add_duelist(interaction: discord.Interaction, duelist_name: str):
    # Checks if the user is registered and if not it will not allow the user to register the duelist
    if not User_db.search(Db_Query.Id == interaction.user.name):
        return_embed = discord.Embed(title=f'User {interaction.user.name} is not registered', colour=discord.Colour.red())
        await interaction.response.send_message(embed=return_embed)
    # In case the user is registered it
    else:
        # it checks the database to know what will be the next duelist id
        if len(Duelist_db.all()) == 0:
            next_id = 1
        else:
            next_id = Duelist_db.all()[-1].doc_id + 1

        # This part gets the information of the user into a user template 
        user_profile = User_template()
        duelist_owner = User_db.search(Db_Query.Id == interaction.user.name)[0]
        user_profile.import_dict(duelist_owner)

        # The information of the new duelist is added to the user profile
        user_profile.Duelist.append(duelist_name)
        user_profile.Duelist_ids.append(next_id)

        # The User information is updated in the database
        update_user_by_name(interaction.user.name,user_profile.export_dict(),User_db,Db_Query)

        # A duelist template is created with the duelist name given by the user, the id the duelist will have in the database and the name of their creator
        # The information is then inserted in the database
        new_duelist = Duelist_template(duelist_name,next_id,interaction.user.name)
        Duelist_db.insert(new_duelist.export_dict())

        # A message is send to confirm that the duelist was registered
        return_embed = discord.Embed(title=f'Duelist {duelist_name} from {interaction.user.name} successfully registered!', colour=discord.Colour.green())
        await interaction.response.send_message(embed=return_embed)
    return
    
@client.tree.command(name="duelist_profile", description="Shows the information of a duelist", guild=GUILD_ID)
async def Find_duelist(interaction: discord.Interaction, duelist_name: str):
    duelist = Duelist_template()
    duelist_data = Duelist_db.search(Db_Query.Name == duelist_name)
    if not duelist_data:
        return_embed = discord.Embed(title=f'Duelist with the name {duelist_name} not found', colour=discord.Colour.red())
        await interaction.response.send_message(embed=return_embed)
    else:
        duelist.import_dict(duelist_data[0])

    return_embed = discord.Embed(title=duelist.name)
    return_embed.add_field(name="Creator", value=duelist.creator, inline=False)
    return_embed.set_thumbnail(url=duelist.icon)
    return_embed.add_field(name="Information", value=duelist.information, inline=False)
    return_embed.add_field(name="Thread", value=duelist.thread, inline=False)
    return_embed.add_field(name="Gelta", value=duelist.gelta, inline=False)
    return_embed.add_field(name="Medium", value=f'{"Animated "if duelist.medium["Animated"] else ""}{"Comic "if duelist.medium["Comic"] else ""}{"Written "if duelist.medium["Written"] else ""}', inline=False)
    return_embed.add_field(name="Win/Loss/Tie", value=f'{duelist.win_loss_tie[0]} / {duelist.win_loss_tie[1]} / {duelist.win_loss_tie[2]}', inline=False)

    await interaction.response.send_message(embed=return_embed)


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
    

@client.tree.command(name="user_profile", description="Shows the information of your profile or the profile of someone else", guild=GUILD_ID)
async def user_profile(interaction: discord.Interaction, discord_tag: str = ""):
    if not discord_tag:
        search = User_db.search(Db_Query.Id == interaction.user.name)
        if not search:
            return_embed = discord.Embed(title=f'User {interaction.user.name} is not registered', colour=discord.Colour.red())
            await interaction.response.send_message(embed=return_embed)
            return
        else:
            UserCheck = User_template()
            UserCheck.import_dict(search[0])
    else:
        search = User_db.search(Db_Query.Id == discord_tag)
        if not search:
            return_embed = discord.Embed(title=f'User {discord_tag} is not registered', colour=discord.Colour.red())
            await interaction.response.send_message(embed=return_embed)
            return
        else:
            UserCheck = User_template()
            UserCheck.import_dict(search[0])

    gelta_count = 0
    Win_count = 0
    Loss_count = 0
    Tie_count  = 0
    Duelist_info = []
    for each in UserCheck.Duelist_ids:
        Duelist = Duelist_db.get(doc_id=each)
        gelta_count += Duelist["Gelta"]
        Win_count += Duelist["Win_Loss_Tie"][0]
        Loss_count += Duelist["Win_Loss_Tie"][1]
        Tie_count += Duelist["Win_Loss_Tie"][2]
        Duelist_name = Duelist["Name"]
        Duelist_thread = Duelist["Thread"]
        Duelist_info.append([Duelist_name,Duelist_thread])
    
    cierite_total = 0
    for each in UserCheck.Cierites:
        if is_iterable(UserCheck.Cierites[each]):
            for each2 in UserCheck.Cierites[each]:
                cierite_total += each2
        else:
            cierite_total += UserCheck.Cierites[each]

    return_embed = discord.Embed(title=UserCheck.Id)
    return_embed.set_thumbnail(url=UserCheck.icon_url)
    return_embed.add_field(name="Gelta Count", value=gelta_count, inline=False)
    return_embed.add_field(name="Wins", value=Win_count)
    return_embed.add_field(name="Losses", value=Loss_count)
    return_embed.add_field(name="Ties", value=Tie_count)
    return_embed.add_field(name="Cierites", value=cierite_total, inline=False)
    for each in Duelist_info:
        return_embed.add_field(name=each[0], value=each[1] if each[1] else "No thread link", inline=False)


    await interaction.response.send_message(embed=return_embed)

@client.tree.command(name="edit_duelist", description="Edit your duelist information", guild=GUILD_ID)
async def user_profile(interaction: discord.Interaction, duelist: str, edit_gelta: int = 0, edit_icon: str = "", edit_thread: str = "", edit_info: str = "", add_win: int = 0, add_loss: int = 0, add_tie: int = 0, reset_win_ratio: bool = False, change_animated: bool = False, change_comic: bool = False, change_written: bool = False):
    # Check if user is registered
    search = User_db.search(Db_Query.Id == interaction.user.name)
    if not search:
        return_embed = discord.Embed(title=f'User {interaction.user.name} is not registered', colour=discord.Colour.red())
        await interaction.response.send_message(embed=return_embed)
        return
    else:
        UserCheck = User_template()
        UserCheck.import_dict(search[0])

    if not UserCheck.Duelist:
        return_embed = discord.Embed(title=f'User {interaction.user.name} does not own any duelist', colour=discord.Colour.red())
        await interaction.response.send_message(embed=return_embed)
        return
    else:
        own_duelist = False
        for i in range(len(UserCheck.Duelist)):
            if UserCheck.Duelist[i] == duelist:
                own_duelist = True
                duelist_search_id = UserCheck.Duelist_ids[i]
                break
        if not own_duelist:
            return_embed = discord.Embed(title=f'User {interaction.user.name} do not own any duelist named {duelist}', colour=discord.Colour.red())
            await interaction.response.send_message(embed=return_embed)
            return
        else:
            Duelist_data = Duelist_template()
            Duelist_data.import_dict(Duelist_db.get(doc_id=duelist_search_id))

    if edit_gelta:
        Duelist_data.gelta = edit_gelta
    if edit_icon:
        Duelist_data.icon = edit_icon
    if edit_thread:
        Duelist_data.thread = edit_thread
    if edit_info:
        Duelist_data.information = edit_info
    if add_win:
        Duelist_data.win_loss_tie[0] += add_win
    if add_loss:
        Duelist_data.win_loss_tie[1] += add_loss
    if add_tie:
        Duelist_data.win_loss_tie[2] += add_tie
    if reset_win_ratio:
        Duelist_data.win_loss_tie = [0,0,0]
    if change_animated:
        if Duelist_data.medium["Animated"]:
            Duelist_data.medium["Animated"] = False
        else:
            Duelist_data.medium["Animated"] = True
    if change_comic:
        if Duelist_data.medium["Comic"]:
            Duelist_data.medium["Comic"] = False
        else:
            Duelist_data.medium["Comic"] = True
    if change_written:
        if Duelist_data.medium["Written"]:
            Duelist_data.medium["Written"] = False
        else:
            Duelist_data.medium["Written"] = True

    try:
        update_duelist_by_id(duelist_search_id,Duelist_data.export_dict(),Duelist_db)
    except Exception as e:
        return_embed = discord.Embed(title=f'Error updating the duelist: {e}', colour=discord.Colour.red())
        await interaction.response.send_message(embed=return_embed)
        return
    
    return_embed = discord.Embed(title=f'Duelist {duelist} from {interaction.user.name} successfully eddited!', colour=discord.Colour.green())
    await interaction.response.send_message(embed=return_embed)    
    return

client.run(Bot_Token)
