import discord
import requests
import random
import asyncio
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# GitHub raw URLs
WHITELIST_URL = "https://raw.githubusercontent.com/FemboyNex/FemboyNex.github.io/refs/heads/main/id.txt"
KEYS_URL = "https://raw.githubusercontent.com/FemboyNex/FemboyNex.github.io/refs/heads/main/access.txt"

# Intents setup
intents = discord.Intents.default()
intents.message_content = True  # Add this line
client = discord.Client(intents=intents)

async def get_whitelist():
    try:
        response = requests.get(WHITELIST_URL)
        if response.status_code == 200:
            whitelist = response.text.splitlines()
            print(f"Whitelist: {whitelist}")  # Debugging
            return whitelist
        return []
    except Exception as e:
        print(f"Error fetching whitelist: {e}")
        return []

async def get_keys():
    try:
        response = requests.get(KEYS_URL)
        if response.status_code == 200:
            keys = response.text.splitlines()
            print(f"Keys: {keys}")  # Debugging
            return keys
        return []
    except Exception as e:
        print(f"Error fetching keys: {e}")
        return []

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.content.startswith(".getbadge"):
        user_id = str(message.author.id)
        whitelist = await get_whitelist()
        
        if user_id in whitelist:
            keys = await get_keys()
            if keys:
                key = random.choice(keys)
                keys.remove(key)
                
                embed = discord.Embed(
                    title="🎉 Congratulations! 🎉",
                    description=f"You have received a special key!",
                    color=discord.Color.blue()
                )
                embed.add_field(name="🔑 Your Key:", value=f"`{key}`", inline=False)
                embed.set_footer(text="Do NOT Give Anyone This Key\nThis key gives you access to the mod.\nAsk @femboy.nexxie for help if you dont understand. (I'm going to guess you dont)")
                
                dm_embed = discord.Embed(
                    title="✅ Access Key Sent!",
                    description=f"{message.author.mention}, You are a Graffiti Badge!\nAn access key has been sent to your dms! 📩",
                    color=discord.Color.green()
                )
                
                await message.author.send(embed=embed)
                await message.channel.send(embed=dm_embed)
            else:
                await message.channel.send("No keys available at the moment.")
        else:
            await message.channel.send("You are not whitelisted.")

client.run(TOKEN)
