#!/usr/bin/env python3
"""
3-concurrent.py
Run multiple database queries concurrently using asyncio.gather and aiosqlite.
"""
import asyncio
import aiosqlite

DB_PATH = 'users.db'

async def async_fetch_users():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print('All users:', all_users)
    print('Users older than 40:', older_users)

if __name__ == '__main__':
    asyncio.run(fetch_concurrently())

