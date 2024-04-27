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
        130: ["ACT_4", "ANGEL_SIDE", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        131: ["ACT_4", "DEMON_SIDE", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        132: ["ACT_4", "ANGEL_SIDE", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        133: ["ACT_4", "DEMON_SIDE", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        134: ["ACT_4", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED", "HAS_PVE_REPUTATION_ENABLED"],
        151: ["ACT_4", "ANGEL_SIDE", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        152: ["ACT_4", "DEMON_SIDE", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED"],
        153: ["ACT_4", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED", "HAS_IMMUNITY_ON_MAP_CHANGE_ENABLED", "HAS_SEALED_VESSELS_DISABLED", "HAS_PVE_REPUTATION_ENABLED"],
        154: ["ACT_4", "HAS_PVP_FACTION_ENABLED", "HAS_DROP_DIRECTLY_IN_INVENTORY_ENABLED"]
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
                map_id == 147,
                flags
            )
            # act 4 maps, must be in a separate files
            if map_id in [130, 131, 132, 133, 134, 151, 152, 153, 154]:
                fc_maps.append(map_dto)
            else:
                maps.append(map_dto)
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

    def get_flags(self, map_id):
        return self.FLAG_DEFINITIONS.get(map_id, [])