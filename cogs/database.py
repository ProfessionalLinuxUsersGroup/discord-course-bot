import logging, discord, os
import sqlite3 as db
from discord.ext import commands
from discord import app_commands


# Most efficient insert/update SQL statement, updates or inserts in single operation.
# Requires keys to be unique. Statement should target user IDs when updating/inserting
#
# INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...)
# ON DUPLICATE KEY UPDATE column1 = value1, column2 = value2, ...;

# Reloading via bot.reload_extension() requires re-importing libraries/modules

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test-db-insert", description="test inserting data values, inserts or returns db values from invoker")
    async def test_insert(self, interaction: discord.Interaction):
        logging.info('test-db-insert cog invoked')
        try:
            with db.connect('user.db') as c:
                check = c.execute(
                    "SELECT id FROM user WHERE id = ?", (interaction.user.id,)).fetchone()
                if check is None:
                    c.execute("INSERT INTO user(id, username) VALUES (?,?)",
                              (interaction.user.id,
                               interaction.user.name,)
                    )
                    c.commit()
                    logging.info(f'Name:{interaction.user.name}, ID:{interaction.user.id} inserted into user.db')
                    await interaction.response.send_message(f'DB:{interaction.user.name} inserted into database.')
                else:
                    logging.info(f'Name:{interaction.user.name}, ID:{interaction.user.id} already exist within user.db')
                    await interaction.response.send_message(f'DB:{interaction.user.name} already exists within the database.')
        except db.Error as e:
            print(e)
            logging.error(e)
        except OSError as e:
            print(e)
            logging.error(e)
        except Exception as e:
            print(e)
            logging.error(e)

    @app_commands.command(name="test-return-db-query", description="attempts to return db values from input")
    async def test_return(self, interaction: discord.Interaction, query: str):
        logging.info(f'test-return-db-query command invoked')
        with db.connect('user.db') as c:
            check = c.execute(
                "SELECT id,username FROM user WHERE username LIKE (?)", (f"%{query}%",)).fetchone()
            if check:
                logging.info(f'Name:{check[1]}, ID:{check[0]} found in user.db')
                await interaction.response.send_message(f'DB - Name:{check[1]}, ID:{check[0]} found in user.db.')
            else:
                logging.info(f'Name:{query} absent from user.db')
                await interaction.response.send_message(f'DB:{query} absent from user.db.')

    @commands.command(name="test-insert-msgs")
    async def test_msg_insert(self, ctx: commands.Context):
        logging.info(f'test-insert-msgs command invoked')
        threads = await ctx.guild.active_threads()
        for thread in threads:
            async for msg in thread.history(limit=2):
                await ctx.send(
                    f'Message ID: {msg.id}\n'
                    f'Author ID: {msg.author.id}\n'
                    f'Author Name: {msg.author.name}\n'
                    f'Created at: {msg.created_at}\n'
                    f'Content: {msg.content}\n'
                    f'Word Count: {len(msg.content.split())}\n'
                    f'Thread Name: {thread.name}',
                    ephemeral=True)

async def setup(bot):
    try:
        if not os.path.exists('user.db'):
            open('user.db', 'a').close()
            logging.info(f'DB: attempting to create user.db file.')
            with db.connect('user.db') as c:
                c.executescript(
                    """
                    BEGIN;
                    CREATE TABLE user(
                        id INTEGER PRIMARY KEY,
                        username TEXT
                    );
                    CREATE TABLE messages(
                        userid INTEGER,
                        content TEXT,
                        word_count TEXT,
                        date TEXT,
                        unit INTEGER,
                        FOREIGN KEY (userid) REFERENCES user(id)
                    );
                    COMMIT;
                    """
                )
                c.execute(
                    'CREATE INDEX IF NOT EXISTS idx_userid ON user (id);'
                )
                c.commit()
                logging.info(f'DB: table and index setup successful')

    except db.Error as e:
        print(e)
        logging.error(e)
    except OSError as e:
        print(e)
        logging.error(e)
    except Exception as e:
        print(e)
        logging.error(e)

    await bot.add_cog(Database(bot))
