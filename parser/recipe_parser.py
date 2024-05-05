from typing import List
from dto.recipe_dto import RecipeDto

class RecipeParser:
    def insert_recipes(self, packet_list: List[List[str]]):
        map_npc_id = 0
        item_vnum = 0
        recipes = []
        producer_item_vnum = 0
        is_item = False

        for current_packet in packet_list:
            if len(current_packet) > 1 and current_packet[0] == "##" and current_packet[1] == "scroll":
                is_item = True

            if len(current_packet) > 2 and current_packet[0] == "pdtse":
                item_vnum = int(current_packet[2])
                continue

            if len(current_packet) > 4 and current_packet[0] == "n_run":
                map_npc_id = int(current_packet[4])
                continue

            if current_packet[0] == "m_list" and current_packet[1] == "2" and is_item:
                producer_item_vnum = int(current_packet[2])
                map_npc_id = None

            if current_packet[0] == "m_list" and (current_packet[1] == "3" or current_packet[1] == "6"):
                items = []
                for i in range(2, len(current_packet), 2):
                    if int(current_packet[i + 1]) != -1:
                        vnum = int(current_packet[i + 1])
                        quantity = int(current_packet[i])
                        items.append({"item_vnum": vnum, "quantity": quantity})

                recipe = next((r for r in recipes if r.item_vnum == item_vnum), None)
                if recipe is None:
                    recipe = RecipeDto(item_vnum=item_vnum, quantity=1, items=items,
                                       producer_map_npc_id=map_npc_id, producer_item_vnum=producer_item_vnum)
                    recipes.append(recipe)
                else:
                    recipe.items.extend(items)

        return recipes
