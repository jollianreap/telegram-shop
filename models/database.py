import asyncio
import aiosqlite
import datetime


async def new_db():
    """
    new_db() is function, creating all tables

    """
    async with aiosqlite.connect(r'bot.db') as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS "user" (
        id INTEGER PRIMARY KEY,
        "name" TEXT,
        "username" TEXT,
        "is_admin" BOOLEAN,
        "created_at" DATE
        );
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS "categories" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "category_name"	TEXT
        );
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS "products" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT,
        "description" TEXT,
        "price" FLOAT,
        "link" TEXT NOT NULL,
        "category_id" INTEGER NOT NULL,
        FOREIGN KEY(category_id) REFERENCES categories(id)
        );
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS "transactions" (
        "id" INTEGER PRIMARY_KEY,
        "product_id" INTEGER NOT NULL,
        "buyer_id" INTEGER NOT NULL,
        "is_paid" BOOLEAN NOT NULL,
        "created_at" DATE,
        FOREIGN KEY(product_id) REFERENCES products(id)
        FOREIGN KEY(buyer_id) REFERENCES users(id)
        );
        """)
        await db.commit()


# вытаскивает все записи из заданной таблицы
async def select_all(table, columns: list = None):
    """
    select_all() is a fucntion, which will select all rows from table.
    If you want to see only some columns, pass them in colums argument

    :param  table: str, table you want to be selected
            columns: list, columns you want to see in output

    :return rows: list of tuples, selected rows
    """
    async with aiosqlite.connect('bot.db') as db:
        if columns:
            query = 'SELECT '
            query += ''.join([f'{item}, ' for item in columns]) # перечисляет все колонки
            query = query[:-2] # убирает последнюю запятую
            query += f' FROM {table}'
        else:
            query = f"SELECT * FROM {table}"

        cursor = await db.execute(query)
        rows = await cursor.fetchall()
        await cursor.close()

        return rows


async def select_one(table, filter_field, value):
    """
    select_one() will return you one row filtered by arguments you pass into
    function

    :param  table: str, table you want to be selected
            filter_field: str, column, which will be passed after WHERE expression in SQL
            value: int, str, bool: value used to find row in db

    :return rows: tuple, selected row
    """
    async with aiosqlite.connect('bot.db') as db:
        query = f'SELECT * FROM {table} WHERE {filter_field} = {value}'
        cursor = await db.execute(query)
        rows = await cursor.fetchone()
        await cursor.close()

        return rows

async def create_object(table, data):
    """
    create_object() will insert your data into table

    :param  table: str, table where you want your data insert to
            data: dict, key is column, value is your value for each column

    """
    # просто много преобразований строки, чтобы прийти к нормальному виду SQL запроса
    query = f"INSERT INTO {table} ("
    query += ''.join(f'{item}, ' for item in data.keys())
    query = query[:-2]
    query += ') VALUES (' + ''.join(f'?, ' for i in range(len(data.values())))
    query = query[:-2] + ')'

    async with aiosqlite.connect('bot.db') as db:
        await db.execute(query, list(data.values()))
        await db.commit()


async def main():
    await new_db()
    data = {
        'id': 1312412,
        'name': 'Test',
        'username': 'USername',
        'is_admin': True,
        'created_at': datetime.datetime.utcnow()
    }
    print(await select_one('user', filter_field='id', value=1312412))


if __name__ == "__main__":
    asyncio.run(main())
