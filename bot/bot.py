import os
import discord
from discord.ext import commands
import requests
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Bot is ready! Logged in as {bot.user}")

@bot.command(name="ask")
async def ask(ctx, *, query: str):
    """Asks the RAG bot a question."""
    logger.info(f"User {ctx.author} asked: {query}")
    
    async with ctx.typing():
        try:
            # Call backend API
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={"user_id": str(ctx.author.id), "query": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data["answer"]
                sources = data["sources"]
                
                # Create embed
                embed = discord.Embed(
                    title="RAG Assistant Response",
                    description=answer,
                    color=discord.Color.blue()
                )
                if sources:
                    embed.set_footer(text=f"Sources: {', '.join(sources)}")
                
                message = await ctx.send(embed=embed)
                
                # Add reactions for feedback
                await message.add_reaction("👍")
                await message.add_reaction("👎")
            else:
                await ctx.send("❌ Error: Could not reach the core brain. Please try again later.")
                
        except Exception as e:
            logger.error(f"Error in ask command: {str(e)}")
            await ctx.send("❌ An unexpected error occurred. Please contact the administrator.")

@bot.event
async def on_reaction_add(reaction, user):
    """Handles feedback reactions."""
    if user.bot:
        return
        
    if str(reaction.emoji) in ["👍", "👎"]:
        logger.info(f"Feedback received from {user}: {reaction.emoji} for message {reaction.message.id}")
        # Optionally send to backend
        # requests.post(f"{BACKEND_URL}/api/feedback", ...)

if __name__ == "__main__":
    bot.run(TOKEN)
