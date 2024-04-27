from plugin import Plugin
from parser.generic_parser import GenericParser
from parser.map_parser import MapParser

class MapPlugin(Plugin):
    async def process(self, cleaned_lines):
        folder = "./input/"
        cleaned_lines_filtered = [line for line in cleaned_lines if line]
        packet_list = [line for line in cleaned_lines_filtered if line[0] == "at"]

        map_parser = MapParser()
        await map_parser.insert_or_update_maps_async(folder, packet_list)
        print("Map parsed successfully !")
