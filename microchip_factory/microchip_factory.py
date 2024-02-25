#!/usr/bin/env python3
""" Class file for defining objects in the the microchip factory """

class Bot:
    """ Class for bots in a microchip factory """
    def __init__(self, bot_id: int, chips = None):
        self.bot_id = bot_id
        self.chips = chips if chips else []
        self.instruction = None
        self.low_to = None
        self.high_to = None

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(bot_id={self.bot_id}, " \
               f"chips={self.chips}, face_id=d[o_0]b)"

    def receive_chip(self, value: int):
        """ Receives a chip and stores it in the bot """
        self.chips.append(value)

    def set_instructions(self, low_to: tuple, high_to: tuple):
        """ Sets instruction. Takes in 2 tuples, each with the type of recepient 
        (output or bot) and the microchip-id. Eg.: 
        low_to = ('bot', 130), high_to = ('output', 88). """
        self.low_to = low_to
        self.high_to = high_to


    def act(self, bots: dict, outputs: list):
        """ When a bot has 2 microchips, it will distribute both microchips in a transaction.
        The recepient of the microchip is either another bot or an output, depending on the
        given instructions """
        self.chips.sort()
        # pylint: disable=unbalanced-tuple-unpacking
        low, high = self.chips
        # Process low chip
        if self.low_to[0] == 'bot':
            bots[self.low_to[1]].receive_chip(low)
        else:
            outputs[self.low_to[1]] = low
        # Process high chip
        if self.high_to[0] == 'bot':
            bots[self.high_to[1]].receive_chip(high)
        else:
            outputs[self.high_to[1]] = high
        self.chips = []


class MicroChipFactory:
    """ Factory class for instructing bots handling microchips """
    def __init__(self, target_low: int = None, target_high: int = None):
        self.bots = {}
        self.outputs = {}
        self.responsible_bot = None
        self.target_low = target_low
        self.target_high = target_high

    def process_instructions(self, instructions_file):
        """ Will iterate through a given instruction file and process it """
        with open(instructions_file, "r", encoding="utf-8") as file:
            input_lines = file.read()
        for instruction in input_lines.strip().split('\n'):
            self.parse_single_instruction(instruction)

    def register_bot(self, bot):
        """ Registers a given bot into the factory """
        if bot.bot_id not in self.bots:
            self.bots[bot.bot_id] = bot

    def get_bot(self, bot_id) -> Bot:
        """ Returns a single bot that is loaded in the factory """
        return self.bots[bot_id]

    def register_chip_transaction(self, instruction):
        """ Loads the chip transactins for a given bot """
        # First make sure to load all mentioned bots in if that didn't happen already
        donor_id = int(instruction[1])
        self.register_bot(Bot(donor_id))
        self.register_bot(Bot(int(instruction[6])))
        self.register_bot(Bot(int(instruction[11])))
        # Then assign a set of instruction to given bot
        self.bots[donor_id].set_instructions(low_to = (instruction[5], int(instruction[6])),
                                             high_to = (instruction[10], int(instruction[11])))

    def parse_single_instruction(self, instruction_line):
        """ Parses a single line of an instruction file """
        instruction = instruction_line.split()
        if instruction[0] != "value":
            self.register_chip_transaction(instruction)
            return
        value = int(instruction[1])
        bot_id = int(instruction[-1])
        if bot_id not in self.bots:
            # If the bot does not exist, create it and add it to the dictionary
            self.register_bot(Bot(bot_id, [value]))
        else:
            self.bots[bot_id].receive_chip(value)

    def execute_instructions(self):
        """ Will execute all loaded instructions. Each iteration it will also check if
        the responsible bot is found """
        while any(len(bot.chips) == 2 for bot in self.bots.values()):
            for bot in self.bots.values():
                if len(bot.chips) != 2:
                    continue
                self.filter_for_wanted_bot(bot)
                bot.act(self.bots, self.outputs)

    def filter_for_wanted_bot(self, bot):
        """ Checks if this is the Droid we're looking for """
        if (self.target_low and self.target_high) and \
              sorted(bot.chips) == [self.target_low , self.target_high]:
            self.responsible_bot = bot

    def get_responsible_bot(self):
        """ Returns the responsible bot if one exists """
        if self.responsible_bot is None:
            raise LookupError("No responsible bot was found.")
        return self.responsible_bot

    def get_outputs(self):
        """ Returns the full output of the executed instructions it these exist """
        if self.outputs is None:
            raise LookupError("No outputs found.")
        return self.outputs
