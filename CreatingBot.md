# Creating a Discord Bot with discord.py

## Installation

To create a Discord bot and setup a development environment with discord.py, please refer to [the slides for this workshop](https://docs.google.com/presentation/d/1P6_EonmytWJQI1XNK5hN7Z9uGZqu5r3KNbyq1u3FTMg/edit?usp=sharing).

Once you've gone through this process, you should have your bot token. Put this in a `.env` file, formatted like so:
```python
TOKEN=YOUR_BOT_TOKEN_HERE
```

## Usage

Let's make a Discord bot! We start out our `main.py` file with the usual boilerplate, including a [Python 3 shebang](https://stackoverflow.com/a/19305076) and [main function](https://stackoverflow.com/a/419185), both for best practice:

```python
#!/usr/bin/env python3

def main():
    # Do initialization here!

if __name__ == "__main__":
    main()
```

There are also some imports that we will be needing:
```python
# For asynchronous facilities.
import asyncio

# For loading the .env file.
import os
from dotenv import load_dotenv

# For Discord API.
import discord
```

[discord.Client](https://discordpy.readthedocs.io/en/stable/api.html#client) is the entrypoint for all of discord.py's functionality. At the top of our file, we create a derived class to modify its behavior:

```python
class MyBot(discord.Client):
```

`discord.Client` has [different events that it listens for](https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events). The `on_ready` coroutine is added to the event loop when the bot is ready to start working. Let's override it with a simple informative message:

```python
async def on_ready(self):
	print('Logged on as {0}!'.format(self.user))
```

This is enough for our `MyBot` class for now. Let's work on putting together our `main` function. We have our token in the `.env` file, and need to retrieve it using the `dotenv` package:

```python
		load_dotenv()
    TOKEN = os.getenv("TOKEN")
```

With our token, we are ready to instantiate the client, and log into Discord:

```python
    bot = MyBot()
    bot.run(TOKEN)
```

Now, we can try out the program. If everything worked, you should see the successful `on_ready` message! Now, for some technical details as to what's going on under the hood:

The [`Client.run()` function](https://discordpy.readthedocs.io/en/stable/api.html#discord.Client.run) is a "blocking call that abstracts away the event loop initialization from you." This enters the default asyncio event loop, and schedules the [`Client.start()` function](https://discordpy.readthedocs.io/en/stable/api.html#discord.Client.start) using the [`asyncio.run_until_complete()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_until_complete) method. `Client.start()` invokes `Client.login()`, which logs into Discord, and then `Client.connect()`, which establishes a [WebSocket](https://en.wikipedia.org/wiki/WebSocket) connection. `Client.connect()` then loops infinitely, with each iteration invoking [a coroutine that fields incoming WebSocket messages](https://github.com/Rapptz/discord.py/blob/c582940401a9ab7f2db1f09efe29ed98075ed153/discord/gateway.py#L476). Since we are using asyncio, though, that coroutine is not running all the time. In fact, even when the event loop *starts* running it, that coroutine will yield its time when it needs to do a task that will take time.

Back to writing code. Let's add another method to our `MyBot` class. This is a coroutine that gets executed whenever a new message is sent:

```python
async def on_message(self, message):
```

Now, this is the best part of making a Discord bot. Just look at how much fun stuff that [Message](https://discordpy.readthedocs.io/en/stable/api.html#discord.Message) exposes!

First, we actually have to disregard messages that are from ourselves:

```python
if message.author == self.user:
  	return
```

This compares the snowflake ID of the message author to our bot ID. Now, we can add a command:

```python
if message.content.startswith(".idea"):
	await message.reply("Okay, so how about this:")	
```

