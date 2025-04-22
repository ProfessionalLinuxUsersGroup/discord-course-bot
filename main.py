#!/usr/bin/env python3

import discord
import asyncio
import os
import logging
from discord.ext import commands
from bot import Bot

# Bot token should be exported in the ./venv/bin/activate script
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot: Bot = Bot()

# Normal bot commands ("!greet")


@bot.command("hi")
async def greet(ctx: commands.Context) -> None:
    logging.info("Greet command invoked.\n")
    await ctx.send(f"Hello, {ctx.author}.")

# Slash commands (/greet)


@bot.tree.command(name="greet", description="Say Hello")
async def greet_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.display_name}")


async def main() -> None:
    async with bot:
        if BOT_TOKEN:
            await bot.start(BOT_TOKEN)
        else:
            raise Exception("No bot token provided.")


if __name__ == '__main__':
    asyncio.run(main())
