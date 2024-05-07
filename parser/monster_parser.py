from typing import List
from dto.monster_dto import MonsterDto

class MonsterParser:
    def insert_monsters(self, packet_list: List[List[str]]):
        map_id = 0
        monsters = []

        for current_packet in packet_list:
            if current_packet[0] == "at" and len(current_packet) > 5:
                map_id = int(current_packet[2])
            
            if current_packet[0] == "in" and current_packet[1] == "3" and int(current_packet[3]) <= 20000:
                monster_id = int(current_packet[2])
                map_monster_id = int(current_packet[3])
                map_x = int(current_packet[4])
                map_y = int(current_packet[5])
                direction = int(current_packet[6]) if current_packet[6] else 0

                monster = MonsterDto(map_id, map_monster_id, monster_id, map_x, map_y)
                monsters.append(monster)

        return self.group_monsters_by_map_id(monsters)
        
    def group_monsters_by_map_id(self, monsters):
        monsters_map = {}
        seen_monsters = {}

        for monster in monsters:
            if monster.map_id not in monsters_map:
                monsters_map[monster.map_id] = []
                seen_monsters[monster.map_id] = set()
                
            if monster.map_monster_id not in seen_monsters[monster.map_id]:
                seen_monsters[monster.map_id].add(monster.map_monster_id)
                monsters_map[monster.map_id].append({
                    "map_monster_id": monster.map_monster_id,
                    "vnum": monster.vnum,
                    "map_x": monster.map_x,
                    "map_y": monster.map_y
                })

        return monsters_map
