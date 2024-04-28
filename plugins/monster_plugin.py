from plugin import Plugin
from parser.monster_parser import MonsterParser
from dto.monster_dto import MonsterDto
import os
import shutil
import yaml

class MonsterPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.monsters = []

    async def process(self, cleaned_lines):
        cleaned_lines_filtered = [line for line in cleaned_lines if line]
        packet_list = [line for line in cleaned_lines_filtered if line[0] in ("in", "mv", "at")]

        monster_parser = MonsterParser()
        monster_groups = monster_parser.insert_monsters(packet_list)

        output_monsters_dir = "./output/map_monster_placement"
        if os.path.exists(output_monsters_dir):
            shutil.rmtree(output_monsters_dir)
        os.makedirs(output_monsters_dir)

        for map_id, monsters_info in monster_groups.items():
            for monster_info in monsters_info:
                monster_dto = MonsterDto(map_id=map_id, **monster_info)
                self.monsters.append(monster_dto)

        self.save_monsters_to_yaml(output_monsters_dir)
        print("Monster parsed successfully !")

    def save_monsters_to_yaml(self, output_dir: str):
        for map_id, monsters in self.monsters_by_map_id().items():
            monsters_info = []
            for monster in monsters:
                monsters_info.append({
                    "map_monster_id": monster.map_monster_id,
                    "vnum": monster.vnum,
                    "map_x": monster.map_x,
                    "map_y": monster.map_y,
                    "can_move": monster.can_move
                })
            yaml_data = yaml.dump({f"map_id": map_id, "monsters": monsters_info}, default_flow_style=False, sort_keys=False)
            with open(os.path.join(output_dir, f"monsters_{map_id}.yaml"), "w") as yaml_file:
                yaml_file.write(yaml_data)

    def monsters_by_map_id(self):
        monsters_map = {}
        for monster in self.monsters:
            if monster.map_id not in monsters_map:
                monsters_map[monster.map_id] = []
            monsters_map[monster.map_id].append(monster)
        return monsters_map
