from plugin import Plugin
from parser.monster_parser import MonsterParser
from dto.monster_dto import MonsterDto
import os
import shutil
import time
import yaml

class MonsterPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.monsters = []

    async def process(self, cleaned_lines):
        cleaned_lines_filtered = [line for line in cleaned_lines if line]
        packet_list = [line for line in cleaned_lines_filtered if line[0] in ("in", "mv", "c_map")]

        monster_parser = MonsterParser()
        monster_groups = monster_parser.insert_monsters(packet_list)

        output_monsters_dir = "./output/map_monster_placement"
        self.prepare_output_dir(output_monsters_dir)

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
                    "map_y": monster.map_y
                })
            yaml_data = yaml.dump({f"map_id": map_id, "monsters": monsters_info}, default_flow_style=False, sort_keys=False)
            with open(os.path.join(output_dir, f"map_{map_id}_monsters.yaml"), "w") as yaml_file:
                yaml_file.write(yaml_data)

    def prepare_output_dir(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)

        for entry in os.scandir(output_dir):
            target = entry.path
            if entry.is_dir():
                shutil.rmtree(target, ignore_errors=True)
                continue

            for attempt in range(3):
                try:
                    os.chmod(target, 0o666)
                    os.remove(target)
                    break
                except PermissionError:
                    if attempt == 2:
                        raise
                    time.sleep(0.2)

    def monsters_by_map_id(self):
        monsters_map = {}
        for monster in self.monsters:
            if monster.map_id not in monsters_map:
                monsters_map[monster.map_id] = []
            monsters_map[monster.map_id].append(monster)
        return monsters_map
