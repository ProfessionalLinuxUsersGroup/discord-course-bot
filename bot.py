#!/usr/bin/env python3

import asyncio
import logging
import logging.handlers
import os
from datetime import datetime

import discord
from discord.ext import commands

PREFIXES: tuple = "?", "!"
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Bot(commands.Bot):
    def __init__(self) -> None:
        intents: discord.Intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=PREFIXES, intents=intents)
        self.setup_logging()
        self.remove_command("help")
        self.prefixes: tuple = PREFIXES
        self.active_threads: dict
        self.text_channels: dict

    def setup_logging(self) -> None:
        """
        Set up logging for the bot.
        Adds std.err output to logfile and handles basic file rotation,
        2MB max file size, rotates to bot.log.1...5
        TODO - possibly add compression logic for log files
        """

        try:
            if not os.path.exists("./logs/"):
                os.makedirs("logs")

        except OSError as e:
            print(e)
        except Exception as e:
            print(e)

        finally:
            stream_handler: logging.StreamHandler = logging.StreamHandler()

            rotate_handler = logging.handlers.RotatingFileHandler(
                filename='logs/bot.log',
                maxBytes=2000000,
                backupCount=5,
                encoding='utf-8'
            )

            logging.basicConfig(
                level=logging.INFO,
                encoding='utf-8',
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt="%Y-%m-%d %H:%M:%S",
                handlers=[stream_handler,rotate_handler]
            )


    async def on_ready(self) -> None:
        """Called when the bot is ready to start working."""
        print(f"{now} Bot is ready.")
        print(f"{now} Logged in as:{self.user} (ID:{self.user.id})")
        print(f"{now} Connected to {len(self.guilds)} guild(s)")

        self.text_channels = {
            channel.id: channel
            for guild in self.guilds
            for channel in guild.text_channels
        }

        self.active_threads = {
            thread.id: thread
            for guild in self.guilds
            for thread in await guild.active_threads()
        }

        # discord.Thread.fetch_members # -> []discord.ThreadMember
        # discord.ThreadMember.id      # User ID?
        # discord.Thread.fetch_message

        for id, ch in self.text_channels.items():
            print(f"{now} Channel:{ch} ID:{id}")

        for id, th in self.active_threads.items():
            print(f"{now} Thread:{th} ID:{id}")

    async def setup_hook(self) -> None:
        await super().setup_hook()
        await self.tree.sync()
        print(f"{now} Synced application commands.")
