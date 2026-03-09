import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

# Database Setup ========
from tinydb import TinyDB, Query
Duelist_db = TinyDB("DuelistData.json")
User_db = TinyDB("UserData.json")
User = Query()
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
    response = ""
    for each in duelist_list_response:
        response += (f'-Duelist: {each["Name"]}, Thread Link: {each["Thread"]} - \n')
        
    await interaction.response.send_message(response)

client.run(Bot_Token)