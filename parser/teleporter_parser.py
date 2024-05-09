from typing import List
from dto.teleporter_dto import TeleporterDto

class TeleporterParser:
    def insert_teleporters(self, packet_list: List[List[str]]):
        map_teleporters = {}
        current_map_id = 0
        current_teleporters = []

        for current_packet in packet_list:
            if current_packet[0] == "at" and len(current_packet) > 5:
                if current_map_id != 0 and current_teleporters:
                    map_teleporters[current_map_id] = map_teleporters.get(current_map_id, []) + current_teleporters
                    current_teleporters = []
                current_map_id = int(current_packet[2])

            if current_packet[0] == "npc_req":
                map_npc_id = int(current_packet[2])

            if current_packet[0] == "tp" and current_packet[1] == "1" and current_packet[2] == "2073308":
                map_x = int(current_packet[3])
                map_y = int(current_packet[4])

                teleporter = {
                    "map_npc_id": map_npc_id,
                    "map_x": map_x,
                    "map_y": map_y,
                    "type": 1
                }
                if not any(t['map_npc_id'] == map_npc_id for t in current_teleporters):
                    current_teleporters.append(teleporter)

        if current_map_id != 0 and current_teleporters:
            map_teleporters[current_map_id] = map_teleporters.get(current_map_id, []) + current_teleporters

        teleporter_dtos = [TeleporterDto(map_id, teleporters) for map_id, teleporters in sorted(map_teleporters.items())]
        return teleporter_dtos
