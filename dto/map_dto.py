class MapDto:
    def __init__(self, map_id: int, music: int, flags: list):
        self.map_id = map_id
        self.map_vnum = map_id
        self.map_name_id = map_id
        self.music = music
        self.flags = flags

    def __repr__(self):
        return f"MapDto(map_id={self.map_id}, map_vnum={self.map_vnum}, music={self.music}, " \
               f"flags={self.flags})"
