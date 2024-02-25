#!/usr/bin/env python3
""" Script for finding the number of a bot that is responsible for comparing 
2 given microchip values.  """
import argparse
from microchip_factory.microchip_factory import MicroChipFactory

PARSER = argparse.ArgumentParser(description="Script finding responsible bot",
                                 prog="find-responsible-bot")
PARSER.add_argument("low_value",
                    type=int,
                    help="First microchip value")
PARSER.add_argument("high_value",
                    type=int,
                    help="Second microchip value")
PARSER.add_argument("-i", "--input-file",
                    help="Location of the input file",
                    dest='input_file',
                    default="./input.txt")
ARGS = PARSER.parse_args()


def main():
    """ Main entrypoint of find-responsible-bot """
    factory = MicroChipFactory(int(ARGS.low_value), int(ARGS.high_value))
    factory.process_instructions(ARGS.input_file)
    factory.execute_instructions()
    print(f"Found the bot responsible for handling microchips \"{ARGS.low_value}\" and "
          f"\"{ARGS.high_value}\": {factory.get_responsible_bot()}")

if __name__ == '__main__':
    main()
