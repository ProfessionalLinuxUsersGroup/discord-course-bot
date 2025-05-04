import logging, discord, os
import sqlite3 as db
from discord.ext import commands


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test-db-insert')
    async def test_insert(self, ctx):
        logging.info('test-db-insert cog invoked')
        try:
            with db.connect('user.db') as c:
                check = c.execute(
                    'SELECT id FROM user WHERE id = ?', (ctx.author.id,)).fetchone()
                if check is None:
                    c.execute('INSERT INTO user(id, username) VALUES (?,?)',
                              (ctx.author.id,
                               ctx.author.name,)
                    )
                    c.commit()
                    logging.info(f'Name:{ctx.author.name}, ID: {ctx.author.id} inserted into user.db')
                    await ctx.send(f'DB: {ctx.author.name} inserted into database.')
                else:
                    logging.info(f'Name:{ctx.author.name}, ID: {ctx.author.id} already exist within user.db')
                    await ctx.send(f'DB: {ctx.author.name} already exists within the database.')
        except db.Error as e:
            print(e)
            logging.error(e)
        except OSError as e:
            print(e)
            logging.error(e)
        except Exception as e:
            print(e)
            logging.error(e)

    @commands.command(name='test-return')
    async def test_return(self, ctx):
        with db.connect('user.db') as c:
            check = c.execute(
                'SELECT id FROM user WHERE id = ?', (ctx.author.id,)).fetchone()
            if check is not None:
                logging.info(f'Name:{ctx.author.name}, ID: {ctx.author.id} found in user.db')
                await ctx.send(f'DB: {ctx.author.name} found in user.db.')
            else:
                logging.info(f'Name:{ctx.author.name}, ID: {ctx.author.id} absent from user.db')
                await ctx.send(f'DB: {ctx.author.name} absent from user.db.')

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
