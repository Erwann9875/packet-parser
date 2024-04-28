class MonsterDto:
    def __init__(self, map_id: int, map_monster_id: int, vnum: int, map_x: int, map_y: int, can_move: bool):
        self.map_id = map_id
        self.map_monster_id = map_monster_id
        self.vnum = vnum
        self.map_x = map_x
        self.map_y = map_y
        self.can_move = can_move
    
    def __repr__(self):
        return f"MonsterDto(map_id={self.map_id}, map_monster_id={self.map_monster_id}, vnum={self.vnum}, map_x={self.map_x}, map_y={self.map_y}, can_move={self.can_move})"
