class Plugin:
    def process(self, cleaned_lines):
        raise NotImplementedError("Subclasses must implement process()")