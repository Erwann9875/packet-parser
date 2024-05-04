from typing import List
from dto.recipe_dto import RecipeDto

class RecipeParser:
    def insert_recipes(self, packet_list: List[List[str]]):
        recipes = []
        current_recipe = None
        item_vnum_to_insert = 0
        map_npc_id = None

        for packet in packet_list:
            if len(packet) > 2 and packet[0] == "pdtse":
                item_vnum_to_insert = int(packet[2])

            elif len(packet) > 4 and packet[0] == "n_run":
                map_npc_id = int(packet[4])

            elif packet[0] == "m_list":
                if packet[1] == "2":
                    producer_item_vnum = int(packet[2])
                    current_recipe = RecipeDto(item_vnum=item_vnum_to_insert, quantity = 1, producer_item_vnum=producer_item_vnum, producer_map_npc_id=map_npc_id, items=[])
                    recipes.append(current_recipe)

                elif packet[1] == "3":
                    for i in range(3, len(packet), 2):
                        if int(packet[i]) < 0:
                            continue
                        item = {"item_vnum": int(packet[i]), "quantity": int(packet[i + 1])}
                        if current_recipe and not any(item['item_vnum'] == existing['item_vnum'] for existing in current_recipe.items):
                            current_recipe.items.append(item)

        return [recipe for recipe in recipes if recipe.items]
