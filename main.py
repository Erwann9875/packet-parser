#!/usr/bin/env python3

from packet_processor import PacketProcessor
from plugin import Plugin
import asyncio
import os
import sys

plugin_files = [f for f in os.listdir("plugins") if f.endswith(".py")]
processor = PacketProcessor()
for plugin_file in plugin_files:
    plugin_module = plugin_file[:-3]
    module = __import__(f"plugins.{plugin_module}", fromlist=["plugins"])
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin:
            processor.register_plugin(obj)

DEFAULT_INPUT_FILE = os.path.join("input", "packet.txt")


def load_input_lines(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            return file.readlines()
    except UnicodeDecodeError:
        # Fallback for legacy files that are not UTF-8 encoded.
        with open(input_file, 'r', encoding='latin-1') as file:
            lines = file.readlines()
        print(f"Warning: '{input_file}' is not UTF-8 encoded. Decoded using latin-1.")
        return lines


def run(argv=None):
    args = sys.argv[1:] if argv is None else argv

    if args and args[0] in {"-h", "--help"}:
        print("Usage: python main.py [input_file]")
        print("Example: python main.py .\\input\\packet.txt")
        print("If no input file is provided, '.\\input\\packet.txt' is used.")
        return 0

    input_file = args[0] if args else DEFAULT_INPUT_FILE

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        print("Run this parser with a script, for example: python .\\main.py .\\input\\packet.txt")
        return 84

    lines = load_input_lines(input_file)
    asyncio.run(processor.process_packet(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
