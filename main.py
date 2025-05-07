#!/usr/bin/env python3

import asyncio, os, discord
from discord.ext import commands
from datetime import datetime
from bot import Bot

# https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.Interaction

# Bot token should be exported in the ./venv/bin/activate script
BOT_TOKEN = os.environ.get("BOT_TOKEN")
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# permission integer: 53687176192
bot: Bot = Bot()

# Should not need to use this
# @bot.command()
# async def load(ctx: commands.Context, extension: str):
#   await bot.load_extension(f'cogs.{extension}')
#   print(f'{now} {extension} successfully loaded')

# cog unloader command, !unload {cog name}
@bot.command()
async def unload(ctx: commands.Context, extension: str):
  await bot.unload_extension(f'cogs.{extension}')
  print(f'{now} {extension} successfully unloaded')

# cog reloader command, unload then load extension, cogs must be unloaded first to reflect changes
# !reload {cog name}
@bot.command()
async def reload(ctx: commands.Context, extension: str):
  await bot.unload_extension(f'cogs.{extension}')
  await bot.load_extension(f'cogs.{extension}')
  print(f'{now} {extension} successfully re-loaded')

# Tree command for registering a thread as a discussion post
# Access thread id (is channel ID the ID of the forum itself?) -
# interaction.channel_id

# /dp admin 1 1
# @bot.tree.command(name="dp", description="Set thread as a discussion post.")
# async def set_dp(interaction: discord.Interaction, course: str, unit: int, dp_number: int):
#     pass
    # thread_id = interaction.guild.

# @bot.tree.command(name="testing", description="testing for postgres")
# async def test(interaction: discord.Interaction):
#     threads = interaction.guild.threads if interaction.guild else None

async def main() -> None:
    async with bot:
        if BOT_TOKEN:
            for filename in os.listdir('./cogs'):
              if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                await bot.start(BOT_TOKEN)
        else:
            raise Exception("No bot token provided.")

if __name__ == "__main__":
    asyncio.run(main())
