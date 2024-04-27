from typing import List
import os
from pathlib import Path
import asyncio
import logging
from parser.generic_parser import GenericParser
from dto.map_dto import MapDto
from converter import Converter

class MapParser:
    def __init__(self):
        self._file_map_id_dat = os.path.join(os.path.sep, "MapIDData.dat")
        self._folder_map = os.path.join(os.path.sep, "map")

    def parse_dat_async(self, folder: str) -> List[MapDto]:
        generic_parser = GenericParser(folder + self._file_map_id_dat, "DATA 0", 0, [])
        return generic_parser.get_dtos(" ")

    async def insert_or_update_maps_async(self, folder: str, packet_list: List[List[str]]):
        dictionary_id = self.parse_dat_async(folder)
        folder_map = folder + self._folder_map
        dictionary_music = {x[2]: x[7] for x in packet_list if len(x) > 7 and x[0].strip() == "at"}
        maps = []
        for file in Path(folder_map).iterdir():
            map_id = int(file.name)
            map_dto = MapDto(
                map_id,
                int(dictionary_music.get(file.name, 0)),
                map_id == 147
            )
            maps.append(map_dto)
        maps_yaml = Converter.dto_to_yaml(maps)
        return maps_yaml
