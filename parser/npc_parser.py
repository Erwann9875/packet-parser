from typing import List
from dto.npc_dto import NpcDto

class NpcParser:
    def insert_npcs(self, packet_list: List[List[str]]):
        map_id = 0
        npcs = []
        shop_packets = [packet for packet in packet_list if len(packet) > 6 and packet[0] == "shop" and packet[1] == "2"]
        shop_item_packets = [packet for packet in packet_list if packet[0] == "shopping" or packet[0] == "n_inv"]
        effect_req_dict = {int(packet[2]): int(packet[3]) for packet in packet_list if packet[0] == "eff" and len(packet) > 2}
        npc_req_dict = {int(packet[2]): int(packet[3]) for packet in packet_list if packet[0] == "npc_req" and len(packet) > 3}
        mv_packet_dict = {int(packet[2]): int(packet[3]) for packet in packet_list if packet[0] == "mv" and len(packet) > 4}
        tab_dict = {}

        for current_packet in packet_list:
            if current_packet[0] == "at" and len(current_packet) > 5:
                map_id = int(current_packet[2])
            
            if current_packet[0] == "in" and current_packet[1] == "2" and current_packet[12] == "-1" and int(current_packet[3]) <= 20000:
                map_npc_id = int(current_packet[3])
                vnum = int(current_packet[2])
                pos_x = int(current_packet[4])
                pos_y = int(current_packet[5])
                dialog_id = int(current_packet[9])
                can_move = True if current_packet[13] != "1" else None
                direction_facing = int(current_packet[6]) if len(current_packet) > 13 else None
                quest_dialog_id = npc_req_dict.get(map_npc_id, None)
                npc_effect_vnum = effect_req_dict.get(map_npc_id, None)
                npc_can_move = True if mv_packet_dict.get(map_npc_id, None) is not None else None
                set_dialog = quest_dialog_id if quest_dialog_id != dialog_id else None

                npc = NpcDto(map_id=map_id, map_npc_id=map_npc_id, vnum=vnum, 
                              pos_x=pos_x, pos_y=pos_y, dialog_id=dialog_id, effect_vnum = npc_effect_vnum,
                              can_move=npc_can_move, quest_dialog_id=set_dialog, direction_facing=direction_facing)
                npcs.append(npc)
        
        for shop_packet in shop_packets:
            map_npc_id = int(shop_packet[2])
            shop_name = " ".join(shop_packet[6:])
            menu_type = int(shop_packet[4])
            shop_type = int(shop_packet[5])

            for npc in npcs:
                if npc.map_npc_id == map_npc_id:
                    if npc.item_shop is None:
                        npc.item_shop = {
                            "name": shop_name,
                            "menu_type": menu_type,
                            "shop_type": shop_type,
                            "tabs": []
                        }
                    else:
                        npc.item_shop["name"] = shop_name
                        npc.item_shop["menu_type"] = menu_type
                        npc.item_shop["shop_type"] = shop_type
                    break
                    if npc.skill_shop is None:
                        npc.skill_shop = {
                            "name": shop_name,
                            "menu_type": menu_type,
                            "shop_type": shop_type,
                            "tabs": []
                        }
                    else:
                        npc.skill_shop["name"] = shop_name
                        npc.skill_shop["menu_type"] = menu_type
                        npc.skill_shop["shop_type"] = shop_type
                    break
        
        for shop_item_packet in shop_item_packets:
            shop_tab_id = 0
            map_npc_id = 0

            if shop_item_packet[0] == "shopping":
                shop_tab_id = int(shop_item_packet[1])
                map_npc_id = int(shop_item_packet[4])
            
            if shop_item_packet[0] == "n_inv":
                tab = {
                    "shop_tab_id": shop_tab_id,
                    "items": []
                }

                items_data = shop_item_packet[5:]
                for item_data in items_data:
                    if "." not in item_data:
                        item_vnum = int(item_data)
                        for npc in npcs:
                            if npc.map_npc_id in tab_dict:
                                npc.item_shop = None
                        tab["items"].append({"skill_vnum": item_vnum})
                        continue
                    item_info = item_data.split(".")
                    if len(item_info) >= 4:
                        item_vnum = int(item_info[2])
                        for npc in npcs:
                            if npc.map_npc_id in tab_dict:
                                npc.skill_shop = None
                        tab["items"].append({"item_vnum": item_vnum})
                
                map_npc_id = int(shop_item_packet[2])
            
                if map_npc_id not in tab_dict:
                    tab_dict[map_npc_id] = []
                tab_dict[map_npc_id].append(tab)

            for npc in npcs:
                if npc.map_npc_id in tab_dict:
                    if npc.item_shop is not None:
                        npc.item_shop["tabs"] = tab_dict[npc.map_npc_id]
                    if npc.skill_shop is not None:
                        npc.skill_shop["tabs"] = tab_dict[npc.map_npc_id]

        return self.group_npcs_by_map_id(npcs)

    def group_npcs_by_map_id(self, npcs):
        npcs_map = {}
        seen_npcs = {}

        for npc in npcs:
            if npc.map_id not in npcs_map:
                npcs_map[npc.map_id] = []
                seen_npcs[npc.map_id] = set()

            if npc.map_npc_id not in seen_npcs[npc.map_id]:
                seen_npcs[npc.map_id].add(npc.map_npc_id)
                npcs_map[npc.map_id].append({
                    "map_npc_id": npc.map_npc_id,
                    "vnum": npc.vnum,
                    "pos_x": npc.pos_x,
                    "pos_y": npc.pos_y,
                    "dialog_id": npc.dialog_id,
                    "effect_vnum": npc.effect_vnum,
                    "can_move": npc.can_move,
                    "quest_dialog_id": npc.quest_dialog_id,
                    "direction_facing": npc.direction_facing,
                    "item_shop": npc.item_shop
                })

        return npcs_map
