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
                    'SELECT id FROM user WHERE id = ?', (interaction.user.id,)).fetchone()
                if check is None:
                    c.execute('INSERT INTO user(id, username) VALUES (?,?)',
                              (interaction.user.id,
                               interaction.user.name,)
                    )
                    c.commit()
                    logging.info(f'Name:{interaction.user.name}, ID: {interaction.user.id} inserted into user.db')
                    await interaction.response.send_message(f'DB: {interaction.user.name} inserted into database.')
                else:
                    logging.info(f'Name:{interaction.user.name}, ID: {interaction.user.id} already exist within user.db')
                    await interaction.response.send_message(f'DB: {interaction.user.name} already exists within the database.')
        except db.Error as e:
            print(e)
            logging.error(e)
        except OSError as e:
            print(e)
            logging.error(e)
        except Exception as e:
            print(e)
            logging.error(e)

    @app_commands.command(name="test-return", description="attempts to return db values")
    async def test_return(self, interaction: discord.Interaction):
        with db.connect('user.db') as c:
            check = c.execute(
                'SELECT id FROM user WHERE id = ?', (interaction.user.id,)).fetchone()
            if check is not None:
                logging.info(f'Name:{interaction.user.name}, ID: {interaction.user.id} found in user.db')
                await interaction.response.send_message(f'DB: {interaction.user.name} found in user.db.')
            else:
                logging.info(f'Name:{interaction.user.name}, ID: {interaction.user.id} absent from user.db')
                await interaction.response.send_message(f'DB: {interaction.user.name} absent from user.db.')

async def setup(bot):
    try:
        if not os.path.exists('user.db'):
            open('user.db', 'a').close()
            logging.info(f'DB: attempting to create user.db file.')
            with db.connect('user.db') as c:
                c.execute(
                    '''
                    CREATE TABLE user (
                    id TEXT,
                    username TEXT);
                    '''
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
