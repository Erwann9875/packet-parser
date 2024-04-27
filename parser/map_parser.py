from typing import List
import os
from pathlib import Path
import asyncio
import logging
from parser.generic_parser import GenericParser
from dto.map_dto import MapDto
from converter import Converter

class MapParser:
    FLAG_DEFINITIONS = {
        1: ["ACT_1", "HAS_USER_SHOPS_DISABLED", "NOSVILLE", "HAS_SEALED_VESSELS_DISABLED", "HAS_SIGNPOSTS_ENABLED"],
        130: ["ACT_4", "ANGEL_SIDE", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        131: ["ACT_4", "DEMON_SIDE", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        132: ["ACT_4", "ANGEL_SIDE", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        133: ["ACT_4", "DEMON_SIDE", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        134: ["ACT_4", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED", "HAS_PVE_REPUTATION_ENABLED"],
        151: ["ACT_4", "ANGEL_SIDE", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        152: ["ACT_4", "DEMON_SIDE", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        153: ["ACT_4", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED", "HAS_PVE_REPUTATION_ENABLED"],
        154: ["ACT_4", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED"],
        (2, 17): ["ACT_1"],
        (20, 33): ["ACT_Z"],
        (41, 47): ["ACT_3"],
        (49, 84): ["ACT_1"],
        (85, 102): ["ACT_2"],
        (103, 104): ["ACT_1"],
        (105, 118): ["ACT_3"],
        (119, 121): ["ACT_2"],
        (122, 128): ["ACT_3"],
        129: ["ACT_1", "HAS_USER_SHOPS_DISABLED", "HAS_SEALED_VESSELS_DISABLED", "PORT_ALVEUS"],
        145: ["ACT_3", "HAS_USER_SHOPS_DISABLED", "HAS_SIGNPOSTS_ENABLED"],
        146: ["ACT_3", "HAS_USER_SHOPS_DISABLED"],
        147: ["ACT_3"],
        148: ["ANGEL_SIDE"],
        149: ["DEMON_SIDE"],
        (170, 204): ["ACT_5_1"],
        (205, 220): ["ACT_5_2", "HAS_BURNING_SWORD_ENABLED"],
        228: ["ACT_6_1", "HAS_CHAMPION_EXPERIENCE_ENABLED", "HAS_USER_SHOPS_DISABLED", "HAS_SEALED_VESSELS_DISABLED"],
        (229, 232): ["ACT_6_1", "HAS_CHAMPION_EXPERIENCE_ENABLED", "ANGEL_SIDE"],
        (233, 236): ["ACT_6_1", "HAS_CHAMPION_EXPERIENCE_ENABLED", "DEMON_SIDE"],
        (237, 238): ["ACT_6_1", "HAS_CHAMPION_EXPERIENCE_ENABLED", "ANGEL_SIDE"],
        (239, 240): ["ACT_6_1", "HAS_CHAMPION_EXPERIENCE_ENABLED", "DEMON_SIDE"],
        (241, 248): ["ACT_6_2", "HAS_CHAMPION_EXPERIENCE_ENABLED"],
        (249, 251): ["ACT_6_2", "ACT_4"],
        260: ["ACT_3"],
        2006: ["HAS_PVP_ENABLED"],
        2104: ["ACT_1"],
        2106: ["HAS_PVP_FAMILY_ENABLED"],
        2500: ["ACT_2", "HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2510: ["ACT_2", "HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2515: ["HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2520: ["ACT_1", "HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        (2526, 2527): ["ACT_6_1", "HAS_CHAMPION_EXPERIENCE_ENABLED"],
        2530: ["ACT_2", "HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        (2537, 2539): ["ACT_5_2", "HAS_BURNING_SWORD_ENABLED"],
        2540: ["ACT_3", "HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2544: ["HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2550: ["HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2553: ["ACT_5_2", "HAS_BURNING_SWORD_ENABLED", "HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        (2554, 2555): ["ACT_5_2", "HAS_BURNING_SWORD_ENABLED"],
        2556: ["ACT_5_2", "HAS_BURNING_SWORD_ENABLED", "HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        (2557, 2558): ["ACT_5_2", "HAS_BURNING_SWORD_ENABLED"],
        2560: ["HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2580: ["HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2587: ["ACT_5_1", "HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2590: ["ACT_5_1", "HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        (2591, 2593): ["ACT_5_1"],
        (2600, 2602): ["ACT_6_1", "HAS_CHAMPION_EXPERIENCE_ENABLED", "ANGEL_SIDE"],
        (2603, 2605): ["ACT_6_1", "HAS_CHAMPION_EXPERIENCE_ENABLED", "DEMON_SIDE"],
        2612: ["HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2623: ["HAS_RAID_TEAM_SUMMON_STONE_ENABLED"],
        2628: ["ACT_7_1"],
        2650: ["ACT_7_1"],
        20001: ["IS_MINILAND_MAP"],
        (24601, 24607): ["ACT_1"]
    }

    def __init__(self):
        self._file_map_id_dat = os.path.join(os.path.sep, "MapIDData.dat")
        self._folder_map = os.path.join(os.path.sep, "map")

    def parse_dat_async(self, folder: str) -> List[MapDto]:
        generic_parser = GenericParser(folder + self._file_map_id_dat, "DATA 0", 0, [])
        return generic_parser.get_dtos(" ")

    async def insert_or_update_maps_async(self, fc: bool, folder: str, packet_list: List[List[str]]):
        dictionary_id = self.parse_dat_async(folder)
        folder_map = folder + self._folder_map
        dictionary_music = {x[2]: x[7] for x in packet_list if len(x) > 7 and x[0].strip() == "at"}
        maps = []
        fc_maps = []
        for file in Path(folder_map).iterdir():
            map_id = int(file.name)
            flags = self.get_flags(map_id)
            map_dto = MapDto(
                map_id,
                int(dictionary_music.get(file.name, 0)),
                flags
            )
            # act 4 maps, must be in a separate files
            if map_id in [130, 131, 132, 133, 134, 151, 152, 153, 154]:
                fc_maps.append(map_dto)
            else:
                maps.append(map_dto)
        maps.sort(key=lambda x: x.map_id)
        fc_maps.sort(key=lambda x: x.map_id)
        maps_yaml = None
        if not fc:
            maps_yaml = Converter.dto_to_yaml(maps)
        else:
            maps_yaml = Converter.dto_to_yaml(fc_maps)
        return maps_yaml
    
    def add_map_flag(map_id: int, flag: str):
        if map_id in FLAG_DEFINITIONS:
            FLAG_DEFINITIONS[map_id].append(flag)
        else:
            FLAG_DEFINITIONS[map_id] = [flag]

    def get_flags(self, map_id: int):
        flags = []
        for key in self.FLAG_DEFINITIONS:
            if isinstance(key, tuple) and len(key) == 2 and key[0] <= map_id <= key[1]:
                flags.extend(self.FLAG_DEFINITIONS[key])
            elif key == map_id:
                flags.extend(self.FLAG_DEFINITIONS[key])
        return flags