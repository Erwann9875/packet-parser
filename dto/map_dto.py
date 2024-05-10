class MapDto:
    def __init__(self, map_id: int, map_music_id: int, flags: list):
        self.map_id = map_id
        self.map_vnum = map_id
        self.map_name_id = map_id
        self.map_music_id = map_music_id
        self.flags = flags

    def __repr__(self):
        return f"MapDto(map_id={self.map_id}, map_vnum={self.map_vnum}, map_music_id={self.map_music_id}, " \
               f"flags={self.flags})"
