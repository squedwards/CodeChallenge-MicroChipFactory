""" Test MicroChip Factory"""
import unittest
from microchip_factory.microchip_factory import Bot, MicroChipFactory

class TestBot(unittest.TestCase):
    """ Class for testing the Bot Class """
    def test_receive_chip(self):
        """ Test that a chip is correctly received and stored by a bot """
        bot = Bot(bot_id=1)
        bot.receive_chip(5)
        self.assertIn(5, bot.chips)

    def test_set_instructions(self):
        """ Test that instructions are correctly set for a bot """
        bot = Bot(bot_id=1)
        bot.set_instructions(low_to=('bot', 2), high_to=('output', 1))
        self.assertEqual(bot.low_to, ('bot', 2))
        self.assertEqual(bot.high_to, ('output', 1))

    def test_act_distributes_chips_correctly(self):
        """ Test that a bot correctly distributes chips according to its instructions """
        factory = MicroChipFactory()
        bot1 = Bot(bot_id=1, chips=[5, 3])
        bot2 = Bot(bot_id=2)
        factory.bots[1] = bot1
        factory.bots[2] = bot2
        bot1.set_instructions(low_to=('bot', 2), high_to=('output', 0))
        bot1.act(factory.bots, factory.outputs)
        self.assertEqual(factory.bots[2].chips, [3])
        self.assertEqual(factory.outputs[0], 5)

class TestMicroChipFactory(unittest.TestCase):
    """ Class for testing the MicroChipFactory Class """
    def setUp(self):
        """Initialize a new MicroChipFactory instance for each test method """
        self.factory = MicroChipFactory()
        self.factory.process_instructions("./input.txt")

    def test_get_bot(self):
        """ Test that a bot can be correctly retrieved from the MicroChipFactory """
        bot = Bot(bot_id=1)
        self.factory.bots[1] = bot
        retrieved_bot = self.factory.get_bot(1)
        self.assertEqual(retrieved_bot, bot)

    def test_execute_instructions_identifies_responsible_bot(self):
        """ Test that executing instructions identifies the responsible bot when it 
        processes the target chips """
        self.factory.target_low = 17
        self.factory.target_high = 61
        self.factory.execute_instructions()
        self.assertEqual(self.factory.responsible_bot.bot_id, 73)

    def test_get_outputs(self):
        """ Test that the MicroChipFactory correctly generates outputs after 
        executing instructions """
        bot1 = Bot(bot_id=1, chips=[2, 5])
        bot2 = Bot(bot_id=2)
        self.factory.bots[1] = bot1
        self.factory.bots[2] = bot2
        bot1.set_instructions(low_to=('bot', 2), high_to=('output', 0))
        self.factory.execute_instructions()
        self.assertIn(0, self.factory.outputs)
        self.assertEqual(self.factory.outputs[0], 5)

if __name__ == '__main__':
    unittest.main()
