import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print("ERROR: No TOKEN env var!")
    exit(1)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    for guild in bot.guilds:
        if guild.system_channel:
            await guild.system_channel.send(f'Hello {guild.name}! I\'m online and ready.')
    if not keep_threads_alive.is_running():
        keep_threads_alive.start()

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel:
        await guild.system_channel.send(f'Welcome {member.mention}! Enjoy your stay in **{guild.name}**!')

@bot.command(name='testjoin')
@commands.has_permissions(administrator=True)
async def test_join(ctx):
    await on_member_join(ctx.author)
    await ctx.send("Join event simulated! Check system channel.")

@tasks.loop(hours=6)
async def keep_threads_alive():
    for guild in bot.guilds:
        for channel in guild.channels:
            if isinstance(channel, discord.Thread):
                try:
                    thread = await channel.fetch()
                    if thread.last_message_id:
                        last_msg_time = thread.last_message.created_at
                        if datetime.utcnow() - last_msg_time > timedelta(days=5):
                            await thread.send("Thread bump: Still active!")
                            await asyncio.sleep(1)
                            print(f"Bumped: {thread.name} in {guild.name}")
                except Exception as e:
                    print(f"Thread error: {e}")

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
