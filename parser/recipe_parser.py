from typing import List
from dto.recipe_dto import RecipeDto

class RecipeParser:
    def insert_recipes(self, packet_list: List[List[str]]):
        map_npc_id = 0
        item_vnum = 0
        recipes = []

        for current_packet in packet_list:
            if len(current_packet) > 2 and current_packet[0] == "pdtse":
                item_vnum = int(current_packet[2])
                continue

            if len(current_packet) > 4 and current_packet[0] == "n_run":
                map_npc_id = int(current_packet[4])
                continue

            if current_packet[0] == "m_list" and (current_packet[1] == "2" or current_packet[1] == "4"):
                items = []

                for i in range(2, len(current_packet) - 1):
                    vnum = int(current_packet[i])
                    items.append(vnum)
                
                recipe = RecipeDto(item_vnum)
                
