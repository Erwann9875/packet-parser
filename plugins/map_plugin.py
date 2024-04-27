from plugin import Plugin
from parser.generic_parser import GenericParser
from parser.map_parser import MapParser
import os

class MapPlugin(Plugin):
    async def process(self, cleaned_lines):
        folder = "./input/"
        cleaned_lines_filtered = [line for line in cleaned_lines if line]
        packet_list = [line for line in cleaned_lines_filtered if line[0] == "at"]

        map_parser = MapParser()
        maps_yaml = await map_parser.insert_or_update_maps_async(folder, packet_list)

        output_maps_dir = "./output/maps"
        if os.path.exists(output_maps_dir):
            shutil.rmtree(output_maps_dir)

        os.makedirs(output_maps_dir)

        with open(os.path.join(output_maps_dir, "official_maps.yaml"), "w") as yaml_file:
            yaml_file.write(maps_yaml)

        print("Map parsed successfully !")
