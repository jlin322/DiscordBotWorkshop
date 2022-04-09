#!/usr/bin/env python3

import discord

import asyncio
import time


class MyBot(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(".idea"):
            await message.reply("Okay, so how about this:")


def main():
    with open(".token", "r") as token_file:
        token = token_file.read().rstrip()

    print("Working on it...")
    MyBot().run(token)


if __name__ == "__main__":
    main()
