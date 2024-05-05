from plugin import Plugin
from collections import defaultdict
from parser.teleporter_parser import TeleporterParser
import os
import shutil
import yaml

class RecipePlugin(Plugin):
    async def process(self, cleaned_lines):
        cleaned_lines_filtered = [line for line in cleaned_lines if line]
        packet_list = [line for line in cleaned_lines_filtered if line[0] in ("npc_req", "tp", "at")]

        teleporter_parser = TeleporterParser()
        teleporters = teleporter_parser.insert_teleporters(packet_list)

        output_teleporters_dir = "./output/map_teleporters"
        if os.path.exists(output_teleporters_dir):
            shutil.rmtree(output_teleporters_dir)
        os.makedirs(output_teleporters_dir)

        for teleporter in teleporters:
            file_path = os.path.join(output_teleporters_dir, f"map_{teleporter.map_id}_teleporters.yaml")
            with open(file_path, "w") as yaml_file:
                yaml_data = yaml.dump({
                    "map_id": teleporter.map_id,
                    "teleporters": teleporter.teleporters
                }, default_flow_style=False, sort_keys=False)
                yaml_file.write(yaml_data)

        print("Teleporters parsed successfully !")
