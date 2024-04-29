class RecipeDto:
    def __init__(self, item_vnum: int, quantity: int, items: list, producer_map_npc_id: int = None, producer_item_vnum: int = None):
        self.item_vnum = item_vnum
        self.quantity = quantity
        self.producer_map_npc_id = producer_map_npc_id
        self.producer_item_vnum = producer_item_vnum
        self.items = items

    def __repr__(self):
        return f"RecipeDto(item_vnum={self.item_vnum}, quantity={self.quantity}, " \
               f"producer_map_npc_id={self.producer_map_npc_id}, producer_item_vnum={self.producer_item_vnum}, items={self.items})"
