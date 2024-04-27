from plugin import Plugin
from parser.generic_parser import GenericParser

class ExamplePlugin(Plugin):
    def process(self, cleaned_lines):
        print("Example Plugin")
