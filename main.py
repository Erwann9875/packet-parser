#!/usr/bin/env python3

from packet_processor import PacketProcessor
from plugin import Plugin
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    with open(input_file, 'r') as file:
        lines = file.readlines()
    processor.process_packet(lines)
