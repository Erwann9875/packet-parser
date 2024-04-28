from plugin import Plugin
from parser.portal_parser import PortalParser
import os
import shutil
import yaml

class PortalPlugin(Plugin):
    async def process(self, cleaned_lines):
        cleaned_lines_filtered = [line for line in cleaned_lines if line]
        packet_list = [line for line in cleaned_lines_filtered if line[0] in ("at", "gp")]

        portal_parser = PortalParser()
        portal_groups = portal_parser.insert_portals(packet_list)

        output_portals_dir = "./output/map_portals"
        if os.path.exists(output_portals_dir):
            shutil.rmtree(output_portals_dir)

        os.makedirs(output_portals_dir)

        for source_map_id, portals in portal_groups.items():
            yaml_data = self.custom_dto_to_yaml(portals)
            with open(os.path.join(output_portals_dir, f"portals_{source_map_id}.yaml"), "w") as yaml_file:
                yaml_file.write(yaml_data)

        print("Portal parsed successfully !")

    def custom_dto_to_yaml(self, dtos):
        yaml_data = {'portals': []}
        for dto in dtos:
            dto_dict = {}
            for key, value in dto.__dict__.items():
                if isinstance(value, (int, str)):
                    dto_dict[key] = value
            yaml_data['portals'].append(dto_dict)
        return yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)

