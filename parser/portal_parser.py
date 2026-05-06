import os
from typing import List, Dict
from dto.portal_dto import PortalDto

class PortalParser:
    def __init__(self, base_path: str, binary_map_folder: str):
        self.base_path = base_path
        self.binary_map_folder = binary_map_folder
        self.list_portals = []
        self.special_portals = [
            PortalDto(2107, 11, 5, 4, 213, 111, -1), #Pyjama Map
            PortalDto(2108, 11, 5, 5, 16, 56, -1), #SP1 Map
            PortalDto(2109, 11, 5, 11, 8, 107, -1), #SP2 Map
            PortalDto(2111, 11, 5, 22, 5, 30, -1), #SP3 Map
            PortalDto(2112, 11, 5, 46, 11, 43, -1), #SP4 Map
        ]
        self.ignored_portals = {
            (1, 17, 52, 2547, -1),
        }
        self.raid_portal_overrides = {
            (282, 14, 40, 4996, 8): {
                "raid_type": 39,
                "map_name_id": 4996,
            },
            (283, 16, 6, 4996, 8): {
                "raid_type": 40,
                "map_name_id": 4996,
            },
            (2515, 19, 3, 4996, 8): {
                "raid_type": 10,
                "map_name_id": 4996,
            },
            (2547, 23, 6, 4996, 8): {
                "raid_type": 16,
                "map_name_id": 4996,
            },
            (2567, 16, 1, 4996, 8): {
                "raid_type": 16,
                "map_name_id": 4996,
            },
            (2635, 57, 38, 4996, 8): {
                "raid_type": 34,
                "map_name_id": 4996,
            },
            (2636, 20, 22, 4996, 8): {
                "raid_type": 30,
                "map_name_id": 4996,
            },
            (2638, 209, 49, 4996, 8): {
                "raid_type": 31,
                "map_name_id": 4996,
            },
            (2648, 61, 9, 4996, 8): {
                "raid_type": 32,
                "map_name_id": 4996,
            },
        }
    
    def insert_portals(self, packet_list: List[List[str]]):
        map_id = 0
        active_map_id = None
        pending_source_map_id = None
        transition_landings = {}
        portal_groups = {}
        unique_portals = set()

        for special_portal in self.special_portals:
            self.list_portals.append(special_portal)
            unique_portals.add((special_portal.source_map_id, special_portal.source_map_x,
                                special_portal.source_map_y, special_portal.destination_map_id,
                                special_portal.type))
        
        for packet in packet_list:
            if packet[0] == "c_map" and len(packet) > 2:
                packet_map_id = int(packet[2])
                state = int(packet[3]) if len(packet) > 3 else None

                if state == 0:
                    pending_source_map_id = active_map_id if active_map_id is not None else packet_map_id
                else:
                    map_id = packet_map_id
                    active_map_id = packet_map_id
                    pending_source_map_id = None
                continue

            if packet[0] == "at" and len(packet) > 4:
                if pending_source_map_id is not None:
                    destination_map_id = int(packet[2])
                    destination_map_x = int(packet[3])
                    destination_map_y = int(packet[4])

                    if (destination_map_id != pending_source_map_id
                            and (destination_map_x != 0 or destination_map_y != 0)):
                        transition_landings.setdefault(
                            (pending_source_map_id, destination_map_id),
                            set()
                        ).add((destination_map_x, destination_map_y))
                    pending_source_map_id = None
                continue

            if packet[0] == "gp" and len(packet) > 4:
                destination_map_id = int(packet[3])
                source_map_x = int(packet[1])
                source_map_y = int(packet[2])
                portal_type = int(packet[4])

                portal_key = (map_id, source_map_x, source_map_y, destination_map_id, portal_type)
                if portal_key in self.ignored_portals:
                    continue

                portal_tuple = (
                    destination_map_id,  # destination_map_id
                    0,               # source_map_x
                    0,               # source_map_y
                    map_id,          # source_map_id
                    source_map_x,    # destination_map_x
                    source_map_y,    # destination_map_y
                    portal_type      # type
                )

                if portal_type in {12, 3} or map_id in (2108, 2109, 2111, 2112):
                    continue

                if portal_tuple not in unique_portals:
                    portal = PortalDto(*portal_tuple)
                    for attribute, value in self.raid_portal_overrides.get(portal_key, {}).items():
                        setattr(portal, attribute, value)
                    self.list_portals.append(portal)
                    unique_portals.add(portal_tuple)

        paired_portals = set()
        portal_pairs = {}

        for portal in self.list_portals:
            portal_pairs.setdefault((portal.source_map_id, portal.destination_map_id), []).append(portal)

        for (source_map_id, destination_map_id), portals in portal_pairs.items():
            reverse_portals = portal_pairs.get((destination_map_id, source_map_id), [])
            if len(portals) <= 1 or len(portals) != len(reverse_portals):
                continue

            sorted_portals = sorted(portals, key=lambda p: (p.source_map_y, p.source_map_x))
            sorted_reverse_portals = sorted(reverse_portals, key=lambda p: (p.source_map_y, p.source_map_x))

            for portal, reverse_portal in zip(sorted_portals, sorted_reverse_portals):
                portal.destination_map_x = reverse_portal.source_map_x
                portal.destination_map_y = reverse_portal.source_map_y
                reverse_portal.destination_map_x = portal.source_map_x
                reverse_portal.destination_map_y = portal.source_map_y
                paired_portals.add(id(portal))
                paired_portals.add(id(reverse_portal))

        for portal in self.list_portals:
            if id(portal) in paired_portals:
                continue

            if portal.source_map_id == 1 and portal.source_map_x == 117 and portal.source_map_y == 177:
                portal.destination_map_x = 59
                portal.destination_map_y = 2
            reverse_portal = next((p for p in self.list_portals if p.source_map_id == portal.destination_map_id
                                   and p.destination_map_id == portal.source_map_id), None)
            if reverse_portal:
                portal.destination_map_x, portal.destination_map_y = reverse_portal.source_map_x, reverse_portal.source_map_y

        for portal in self.list_portals:
            if portal.destination_map_x != 0 or portal.destination_map_y != 0:
                continue

            pair_key = (portal.source_map_id, portal.destination_map_id)
            portals_for_pair = portal_pairs.get(pair_key, [])
            landing_coordinates = transition_landings.get(pair_key, set())

            if len(portals_for_pair) == 1 and len(landing_coordinates) == 1:
                portal.destination_map_x, portal.destination_map_y = next(iter(landing_coordinates))

        for portal in self.list_portals:
            if portal.source_map_id not in portal_groups:
                portal_groups[portal.source_map_id] = []
            portal_groups[portal.source_map_id].append(portal)

        return portal_groups
