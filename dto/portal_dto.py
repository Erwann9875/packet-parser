class PortalDto:
    def __init__(self, destination_map_id: int, destination_map_x: int, destination_map_y: int,
                 source_map_id: int, source_map_x: int, source_map_y: int, type: int):
        self.destination_map_id = destination_map_id
        self.destination_map_x = destination_map_x
        self.destination_map_y = destination_map_y
        self.source_map_id = source_map_id
        self.source_map_x = source_map_x
        self.source_map_y = source_map_y
        self.type = type

    def to_dict(self):
        return {
            'destination_map_id': self.destination_map_id,
            'destination_map_x': self.destination_map_x,
            'destination_map_y': self.destination_map_y,
            'source_map_id': self.source_map_id,
            'source_map_x': self.source_map_x,
            'source_map_y': self.source_map_y,
            'type': self.type
        }

    def equals(self, other):
        return (self.destination_map_id == other.destination_map_id and
                self.destination_map_x == other.destination_map_x and
                self.destination_map_y == other.destination_map_y and
                self.source_map_id == other.source_map_id and
                self.source_map_x == other.source_map_x and
                self.source_map_y == other.source_map_y and
                self.type == other.type)

    def __repr__(self):
        return (f"PortalDto(source_map_id={self.source_map_id}, "
                f"source_x={self.source_map_x}, source_y={self.source_map_y}, "
                f"destination_map_id={self.destination_map_id}, "
                f"type={self.type}, destination_x={self.destination_map_x}, "
                f"destination_y={self.destination_map_y}")
