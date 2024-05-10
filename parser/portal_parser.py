from typing import List
from dto.portal_dto import PortalDto

class PortalParser:
    def __init__(self):
        self.list_portals2 = []
        self.list_portals1 = []
    
    def insert_portals(self, packet_list: List[List[str]]):
        map_id = 0
        portal_groups = {}

        lod_portal = PortalDto(98, 6, 36, 150, 172, 171, -1)
        miniland_portal = PortalDto(1, 48, 132, 20001, 3, 8, -1)
        wedding_portal = PortalDto(145, 61, 165, 2586, 34, 54, -1)
        glacerus_cavern_portal = PortalDto(189, 48, 156, 2587, 42, 3, -1)

        for special_portal in [lod_portal, miniland_portal, wedding_portal, glacerus_cavern_portal]:
            if not any(portal.source_map_id == special_portal.source_map_id for portal in self.list_portals2):
                self.list_portals2.append(special_portal)
        
        for current_packet in packet_list:
            if current_packet[0] == "at" and len(current_packet) > 2:
                map_id = int(current_packet[2])
                continue

            if current_packet[0] == "gp" and len(current_packet) > 4:
                source_x, source_y = int(current_packet[1]), int(current_packet[2])
                destination_map_id = int(current_packet[3])
                type = int(current_packet[4])

                portal = PortalDto(destination_map_id, 0, 0, map_id, source_x, source_y, type)

                if any(portal.equals(other) for other in self.list_portals1):
                    continue

                self.list_portals1.append(portal)

        self.list_portals1.sort(key=lambda p: (p.source_map_id, p.destination_map_id, p.source_map_y, p.source_map_x))

        for portal in self.list_portals1:
            if not any(portal.equals(other) for other in self.list_portals2):
                p = next((p for p in self.list_portals1 if p.source_map_id == portal.destination_map_id
                          and p.destination_map_id == portal.source_map_id), None)
                if p:
                    portal.destination_map_x, portal.destination_map_y = p.source_map_x, p.source_map_y
                    p.destination_map_x, p.destination_map_y = portal.source_map_x, portal.source_map_y
                self.list_portals2.extend([portal] if p is None else [portal, p])

        for portal in self.list_portals2:
            if portal.source_map_id not in portal_groups:
                portal_groups[portal.source_map_id] = []
            portal_groups[portal.source_map_id].append(portal)

        return portal_groups
