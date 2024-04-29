from plugin import Plugin
from parser.recipe_parser import RecipeParser
import os
import shutil
import yaml

class RecipePlugin(Plugin):
    async def process(self, cleaned_lines):
        cleaned_lines_filtered = [line for line in cleaned_lines if line]
        packet_list = [line for line in cleaned_lines_filtered if line[0] in ("pdtse", "m_list", "pdtclose", "n_run")]

        recipe_parser = RecipeParser()
        recipe_groups = recipe_parser.insert_recipes(packet_list)

        output_recipes_dir = "./output/recipes"
        if os.path.exists(output_recipes_dir):
            shutil.rmtree(output_recipes_dir)
        os.makedirs(output_recipes_dir)

        # for producer_item_vnum, recipes in recipe_groups.items():
        #     yaml_data = self.custom_dto_to_yaml(recipes)
        #     with open(os.path.join(output_recipes_dir, f"recipes_{producer_item_vnum}.yaml"), "w") as yaml_file:
        #         yaml_file.write(yaml_data)

        print("Recipes parsed successfully !")

    # def custom_dto_to_yaml(self, dtos):
    #     yaml_data = {'recipes': []}
    #     for dto in dtos:
    #         for recipe in dto['recipes']:
    #             cleaned_recipe = {key: value for key, value in recipe.items() if key in ['item_vnum', 'quantity', 'producer_map_npc_id', 'items']}
    #             yaml_data['recipes'].append(cleaned_recipe)
    #     return yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)