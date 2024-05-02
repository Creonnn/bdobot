import discord, os, messages
from dotenv import load_dotenv

def run_discord_bot():
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))
    
    @client.event
    async def on_message(message):
        disc_id = str(message.author.id)
        user_message = str(message.content)
        svr_id = str(message.guild.id)

        if message.author == client.user:
            return
        
        if user_message == "!help":
            await message.channel.send(f"```{messages.help}```")

        elif user_message[:2].lower() == "!i" or user_message[:5].lower() == "!item":
            m = user_message[5:].strip().lower() if user_message[:5] == "!item" else user_message[2:].strip().lower()
            await message.channel.send(f"```{messages.item_summary(m)}```")

        elif user_message[:2].lower() == "!p" or user_message[:6].lower() == "!price":
            m = user_message[6:].strip().lower() if user_message[:5] == "!item" else user_message[2:].strip().lower()
            await message.channel.send(f"```{messages.price(m)}```")
    
    load_dotenv()
    client.run(os.getenv('TOKEN'))

