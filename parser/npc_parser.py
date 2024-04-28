from typing import List
from dto.npc_dto import NpcDto

class NpcParser:
    def insert_npcs(self, packet_list: List[List[str]]):
        map_id = 0
        npcs = []

        for current_packet in packet_list:
            if current_packet[0] == "at" and len(current_packet) > 5:
                map_id = int(current_packet[2])
            
            if current_packet[0] == "in" and current_packet[1] == "2" and int(current_packet[3]) <= 20000:
                map_npc_id = int(current_packet[3])
                vnum = int(current_packet[2])
                pos_x = int(current_packet[4])
                pos_y = int(current_packet[5])
                dialog_id = int(current_packet[9])
                can_move = current_packet[13] != "1"
                direction_facing = int(current_packet[6]) if len(current_packet) > 13 else None

                npc = NpcDto(map_id=map_id, map_npc_id=map_npc_id, vnum=vnum, 
                              pos_x=pos_x, pos_y=pos_y, dialog_id=dialog_id, 
                              can_move=can_move, direction_facing=direction_facing)
                npcs.append(npc)

        return self.group_npcs_by_map_id(npcs)

    def group_npcs_by_map_id(self, npcs):
        npcs_map = {}
        for npc in npcs:
            if npc.map_id not in npcs_map:
                npcs_map[npc.map_id] = []
            npcs_map[npc.map_id].append({
                "map_npc_id": npc.map_npc_id,
                "vnum": npc.vnum,
                "pos_x": npc.pos_x,
                "pos_y": npc.pos_y,
                "dialog_id": npc.dialog_id,
                "can_move": npc.can_move,
                "direction_facing": npc.direction_facing
            })
        return npcs_map
