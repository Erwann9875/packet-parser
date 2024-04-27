class MapDto:
    def __init__(self, map_id: int, music: int, data: bytes, shop_allowed: bool):
        self.map_id = map_id
        self.music = music
        self.data = data
        self.shop_allowed = shop_allowed

    def __repr__(self):
        return f"MapDto(map_id={self.map_id}, music={self.music}, " \
               f"data=<{len(self.data)} bytes>, shop_allowed={self.shop_allowed})"
