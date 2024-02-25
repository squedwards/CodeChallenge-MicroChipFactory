#!/usr/bin/env python3
""" Script for finding the number of a bot that is responsible for comparing 
2 given microchip values.  """
import argparse
from microchip_factory.microchip_factory import MicroChipFactory

PARSER = argparse.ArgumentParser(description="Script finding responsible bot",
                                 prog="multiply-output-values")
PARSER.add_argument("outputs",
                    type=str,
                    help="comma-seperated list of the outputs to be multiplied")
PARSER.add_argument("-i", "--input-file",
                    help="Location of the input file",
                    dest='input_file',
                    default="./input.txt")
ARGS = PARSER.parse_args()

def main():
    """ Main entrypoint of multiply-output-values """
    factory = MicroChipFactory()
    factory.process_instructions(ARGS.input_file)
    factory.execute_instructions()
    factory_outputs = factory.get_outputs()
    output_product = 1
    for i in ARGS.outputs.split(','):
        output_product = output_product * factory_outputs[int(i)]
    print("Result of multipling together the values of one chip in outputs "
          f"{ARGS.outputs}: {output_product}")

if __name__ == '__main__':
    main()
