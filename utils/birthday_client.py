import json

import discord

from . import BirthdayJSONDecoder

class BirthdayClient(discord.Client):

    def __init__(self, filepath):

        intents = discord.Intents.all()

        self.filepath = filepath
        with open(filepath, 'r') as fh:
            try:
                self.birthdays = json.load(fh, cls=BirthdayJSONDecoder)
            except json.decoder.JSONDecodeError:
                self.birthdays = {}
        super().__init__(intents = intents)