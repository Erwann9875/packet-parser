class PacketProcessor:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin_cls):
        self.plugins.append(plugin_cls())

    async def process_packet(self, packet):
        cleaned_lines = [line.split()[2:] for line in packet]
        for plugin in self.plugins:
            await plugin.process(cleaned_lines)