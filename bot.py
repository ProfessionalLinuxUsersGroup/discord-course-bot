#!/usr/bin/env python3

import asyncio
import logging
import os

import discord
from discord.ext import commands

PREFIXES: tuple = "?", "!"


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
        Passes in a custom formatter to `discord.utils.setup_logging` to
        customize the format of the log string.
        """

        try:
            if not os.path.exists("./logs/"):
                os.makedirs("logs")

        except OSError as e:
            print(e)
        except Exception as e:
            print(e)

        finally:
            log_format = "%(asctime)s %(name)s %(levelname)-8s: %(message)s"
            date_format = "%Y-%m-%d %H:%M:%S"

            formatter: logging.Formatter = logging.Formatter(
                log_format, datefmt=date_format
            )

            file_handler: logging.FileHandler = logging.FileHandler(
                "logs/bot.log", encoding="utf-8"
            )
            file_handler.setFormatter(formatter)

            stream_handler: logging.StreamHandler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            # File and console logging
            logging.basicConfig(
                level=logging.INFO,
                handlers=[file_handler, stream_handler],
            )

    async def on_ready(self) -> None:
        """Called when the bot is ready to start working."""
        print("Bot is ready.")
        logging.info(f"Logged in as: {self.user} (ID: {self.user.id})")
        logging.info(f"Connected to {len(self.guilds)} guild(s)")

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
            logging.info(f"Channel: {ch}")
            logging.info(f"ID: {id}")

        for id, th in self.active_threads.items():
            logging.info(f"Thread: {th}")
            logging.info(f"ID: {id}")

        logging.info(f"Text channels: {self.text_channels}")
        logging.info(f"Threads: {self.active_threads}")

    async def setup_hook(self) -> None:
        await super().setup_hook()
        await self.tree.sync()
        logging.info("Synced application commands.")
