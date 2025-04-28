#!/usr/bin/env python3

import discord
import asyncio
import os
import logging
from discord.ext import commands
from bot import Bot

# Bot token should be exported in the ./venv/bin/activate script
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# permission integer: 53687176192

bot: Bot = Bot()

# Normal bot commands ("!greet")


@bot.command("hi")
async def greet(ctx: commands.Context) -> None:
    logging.info("Greet command invoked.\n")
    await ctx.send(f"Hello, {ctx.author}.")


# Slash commands (/greet)
# https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.Interaction


@bot.tree.command(name="greet", description="Say Hello")
async def greet_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.display_name}")


# Tree command for registering a thread as a discussion post
# Access thread id (is channel ID the ID of the forum itself?) -
# interaction.channel_id

# /dp admin 1 1
@bot.tree.command(name="dp", description="Set thread as a discussion post.")
async def set_dp(interaction: discord.Interaction, course: str, unit: int, dp_number: int):
    pass
    # thread_id = interaction.guild.

@bot.tree.command(name="debug", description="Output data gathered on users")
async def debug_user_data(interaction: discord.Interaction, msg: str = ""):

    threads = interaction.guild.threads if interaction.guild else None

    if not threads:
        await interaction.response.send_message(f"Failed to pull threads!")
         
    if msg == "users":
        await interaction.response.send_message(
            f"Visible users: {', '.join(user.name for user in bot.users)}")

    elif msg == "threads":
        await interaction.response.send_message(
            f"Visible active threads: {bot.active_threads}")

    elif msg == "channels":
        await interaction.response.send_message(
            f"Visible text channels: {bot.text_channels}")
        

    else:
        await interaction.response.send_message(
            f"""
            Visible users: {bot.users}
            \nVisible active threads: {bot.active_threads}
            \nVisible text channels: {bot.text_channels}
            """
        )

async def main() -> None:
    async with bot:
        if BOT_TOKEN:
            await bot.start(BOT_TOKEN)
        else:
            raise Exception("No bot token provided.")

if __name__ == "__main__":
    asyncio.run(main())
