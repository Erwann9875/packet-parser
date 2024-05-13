import os
from typing import List, Dict
from dto.portal_dto import PortalDto

class PortalParser:
    def __init__(self, base_path: str, binary_map_folder: str):
        self.base_path = base_path
        self.binary_map_folder = binary_map_folder
        self.list_portals = []
        self.special_portals = [
            PortalDto(98, 6, 36, 150, 172, 171, -1),
        ]
    
    def insert_portals(self, packet_list: List[List[str]]):
        map_id = 0
        portal_groups = {}
        unique_portals = set()

        for special_portal in self.special_portals:
            self.list_portals.append(special_portal)
            unique_portals.add((special_portal.source_map_id, special_portal.source_map_x,
                                special_portal.source_map_y, special_portal.destination_map_id,
                                special_portal.type))
        
        for packet in packet_list:
            if packet[0] == "c_map" and len(packet) > 2:
                map_id = int(packet[2])
                continue

            if packet[0] == "gp" and len(packet) > 4:
                portal_tuple = (
                    int(packet[3]),  # destination_map_id
                    0,               # source_map_x
                    0,               # source_map_y
                    map_id,          # source_map_id
                    int(packet[1]),  # destination_map_x
                    int(packet[2]),  # destination_map_y
                    int(packet[4])   # type
                )

                if int(packet[4]) in {12, 3} or map_id in (145, 2108, 2109, 2111, 2112):
                    continue

                if portal_tuple not in unique_portals:
                    self.list_portals.append(PortalDto(*portal_tuple))
                    unique_portals.add(portal_tuple)

        for portal in self.list_portals:
            reverse_portal = next((p for p in self.list_portals if p.source_map_id == portal.destination_map_id
                                   and p.destination_map_id == portal.source_map_id), None)
            if reverse_portal:
                portal.destination_map_x, portal.destination_map_y = reverse_portal.source_map_x, reverse_portal.source_map_y

        for portal in self.list_portals:
            if portal.source_map_id not in portal_groups:
                portal_groups[portal.source_map_id] = []
            portal_groups[portal.source_map_id].append(portal)

        return portal_groups
