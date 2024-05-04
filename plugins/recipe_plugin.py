from plugin import Plugin
from collections import defaultdict
from parser.recipe_parser import RecipeParser
import os
import shutil
import yaml

class RecipePlugin(Plugin):
    async def process(self, cleaned_lines):
        cleaned_lines_filtered = [line for line in cleaned_lines if line]
        packet_list = [line for line in cleaned_lines_filtered if line[0] in ("pdtse", "m_list", "pdtclose", "n_run")]

        recipe_parser = RecipeParser()
        recipes = recipe_parser.insert_recipes(packet_list)

        recipe_groups = defaultdict(list)
        for recipe in recipes:
            recipe_groups[recipe.producer_map_npc_id].append(recipe)

        output_recipes_dir = "./output/recipes"
        if os.path.exists(output_recipes_dir):
            shutil.rmtree(output_recipes_dir)
        os.makedirs(output_recipes_dir)

        for npc_id, recipes in recipe_groups.items():
            if npc_id is not None:
                yaml_data = self.recipes_to_yaml(recipes)
                file_path = os.path.join(output_recipes_dir, f"npc_{npc_id}_recipes.yaml")
                with open(file_path, "w") as yaml_file:
                    yaml_file.write(yaml_data)

        print("Recipes parsed successfully !")

    def recipes_to_yaml(self, recipes):
        yaml_list = []
        for dto in recipes:
            recipe_dict = {
                "item_vnum": dto.item_vnum,
                "quantity": dto.quantity,
                "producer_map_npc_id": dto.producer_map_npc_id,
                "producer_item_vnum": dto.producer_item_vnum,
                "items": dto.items
            }
            yaml_list.append(recipe_dict)
        return yaml.dump({"recipes": yaml_list}, default_flow_style=False, sort_keys=False)