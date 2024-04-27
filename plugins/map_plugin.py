from plugin import Plugin

class ExamplePlugin(Plugin):
    def process(self, cleaned_lines):
        print("Example Plugin")
