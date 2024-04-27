class MapDto:
    def __init__(self, map_id: int, music: int, shop_allowed: bool):
        self.map_id = map_id
        self.map_vnum = map_id
        self.map_name_id = map_id
        self.music = music
        self.shop_allowed = shop_allowed

    def __repr__(self):
        return f"MapDto(map_id={self.map_id}, map_vnum={self.map_vnum}, music={self.music}, " \
               f"shop_allowed={self.shop_allowed})"
