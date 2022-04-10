#!/usr/bin/env python3

import asyncio
import os

from dotenv import load_dotenv
import discord


class MyBot(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(".idea"):
            await message.reply("Okay, so how about this:")


def main():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    print("Working on it...")
    MyBot().run(TOKEN)


if __name__ == "__main__":
    main()
