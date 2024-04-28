class NpcDto:
    def __init__(self, map_id: int, map_npc_id: int, vnum: int, pos_x: int, pos_y: int, dialog_id: int, can_move: bool, direction_facing: int = None):
        self.map_id = map_id
        self.map_npc_id = map_npc_id
        self.vnum = vnum
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dialog_id = dialog_id
        self.can_move = can_move
        self.direction_facing = direction_facing
    
    def __repr__(self):
        return f"NpcDto(map_id={self.map_id}, map_npc_id={self.map_npc_id}, vnum={self.vnum}, pos_x={self.pos_x}, pos_y={self.pos_y}, dialog_id={self.dialog_id}, can_move={self.can_move}, direction_facing={self.direction_facing})"
