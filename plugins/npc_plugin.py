from plugin import Plugin
from parser.npc_parser import NpcParser
from dto.npc_dto import NpcDto
import os
import shutil
import yaml

class NpcPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.npcs = []

    async def process(self, cleaned_lines):
        cleaned_lines_filtered = [line for line in cleaned_lines if line]
        packet_list = [line for line in cleaned_lines_filtered if line[0] in ("in", "mv", "at", "shop", "shopping", "n_inv", "npc_req", "eff")]

        npc_parser = NpcParser()
        npc_groups = npc_parser.insert_npcs(packet_list)

        output_npcs_dir = "./output/map_npc_placement"
        if os.path.exists(output_npcs_dir):
            shutil.rmtree(output_npcs_dir)
        os.makedirs(output_npcs_dir)

        for map_id, npcs_info in npc_groups.items():
            for npc_info in npcs_info:
                npc_dto = NpcDto(map_id=map_id, **npc_info)
                self.npcs.append(npc_dto)

        self.save_npcs_to_yaml(output_npcs_dir)
        print("Npc parsed successfully !")

    def save_npcs_to_yaml(self, output_dir: str):
        for map_id, npcs in self.npcs_by_map_id().items():
            npcs_info = []
            for npc in npcs:
                npc_info = {
                    "map_npc_id": npc.map_npc_id,
                    "vnum": npc.vnum,
                    "pos_x": npc.pos_x,
                    "pos_y": npc.pos_y,
                    "dialog_id": npc.dialog_id
                }
                if npc.effect_vnum is not None:
                    npc_info["effect_vnum"] = npc.effect_vnum
                if npc.can_move is not None:
                    npc_info["can_move"] = npc.can_move
                if npc.quest_dialog_id is not None:
                    npc_info["quest_dialog_id"] = npc.quest_dialog_id
                if npc.direction_facing is not None:
                    npc_info["direction_facing"] = npc.direction_facing
                if npc.item_shop is not None:
                    npc_info["item_shop"] = npc.item_shop
                if npc.skill_shop is not None:
                    npc_info["skill_shop"] = npc.skill_shop
                npcs_info.append(npc_info)

            yaml_data = yaml.dump({"map_id": map_id, "npcs": npcs_info}, default_flow_style=False, sort_keys=False, allow_unicode=True)
            with open(os.path.join(output_dir, f"map_{map_id}_npc.yaml"), "w") as yaml_file:
                yaml_file.write(yaml_data)

    def npcs_by_map_id(self):
        npcs_map = {}
        for npc in self.npcs:
            if npc.map_id not in npcs_map:
                npcs_map[npc.map_id] = []
            npcs_map[npc.map_id].append(npc)
        return npcs_map
