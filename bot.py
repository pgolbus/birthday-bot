from datetime import datetime, date

import logging
import os
import re

import discord
from dotenv import load_dotenv
import humanize


# Look at all of these beautiful docstrings! Guess who didn't eat their TDD Wheaties!
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

logger = logging.getLogger("discord")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

GENERAL_ID = 1092880161659158542
DATE_REGEX = re.compile("(\d{1,2}\/\d{1,2}\/\d{4})")


def init_logger():
    logger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler(
        filename=f"./discord.log", encoding="utf-8", mode="a"
    )
    fileHandler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)


@client.event
async def on_ready():
    logger.info("connected")


@client.event
async def on_member_join(member):
    logger.info("%s joined" % member.name)
    channel = client.get_channel(GENERAL_ID)
    msg = [f"{member.mention}, welcome to the CS411 Birthday discord server."]
    msg.append(
        'If you @ me your birthday "@birthday-bot MM/DD/YYYY", I will tell you how many days you\'ve been alive.'
    )
    msg.append("I hope something good happens to you today!")
    msg = "\n".join(msg)
    await channel.send(msg)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    logger.info("%s %s" % (message.mentions, message.content))

    at_me = any([mention.name == "cs411-birthday-bot" for mention in message.mentions])

    if at_me:
        logger.info("%s" % message.content)
        try:
            date_string = re.search(DATE_REGEX, message.content)[0]
            logger.info("%s" % date_string)
            birthday = datetime.strptime(date_string, "%m/%d/%Y").date()
            response = date_message(birthday)
            await message.channel.send(response)
        except TypeError:
            await message.channel.send("DEATH!")
            # await message.channel.send(
            #     " ".join(
            #         [
            #             "I hope something good happens to you today.",
            #             'If you tell me your birthday "@cs411-birthday-bot MM/DD/YYYY",',
            #             "I'll tell you how many days you've been alive.",
            #         ]
            #     )
            # )


def days_ago(birthday):
    today = date.today()
    delta = today - birthday
    return delta, int(re.search("\d+", str(delta))[0])


def date_message(birthday):
    logger.info("%s" % str(birthday))
    delta, days = days_ago(birthday)
    if days <= 31:
        return f"That's {days} days!"
    return f"{humanize.intcomma(days)} days. That's {humanize.precisedelta(delta)}!"


if __name__ == "__main__":
    init_logger()
    client.run(DISCORD_BOT_TOKEN)
