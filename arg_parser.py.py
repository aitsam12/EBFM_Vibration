## feel free to add more arguments

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Vibration estimation sample.')
    parser.add_argument('-i', '--input', type=str, help='Input file path.')
    parser.add_argument('-o', '--output', type=str, help='Output video file path.')
    return parser.parse_args()
