import logging, discord, os
import sqlite3 as db
from discord.ext import commands
from discord import app_commands

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # These commands can potentially take up to an hour to register in discord when using '/' commands
    @app_commands.command(name="test-db-insert", description="test inserting data values, inserts or returns db values")
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
        with db.connect('user.db') as c:
            check = c.execute(
                "SELECT id,username FROM user WHERE username LIKE (?)", (f"%{query}%",)).fetchone()
            if check:
                logging.info(f'Name:{check[1]}, ID:{check[0]} found in user.db')
                await interaction.response.send_message(f'DB - Name:{check[1]}, ID:{check[0]} found in user.db.')
            else:
                logging.info(f'Name:{query} absent from user.db')
                await interaction.response.send_message(f'DB:{query} absent from user.db.')

    # @app_commands.command(name="test-insert-msgs", description="attempts to insert messages based on user")
    # async def test_msg_insert(self, interaction: discord.Interaction):
    #     for thread in self.bot.active_threads:

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
