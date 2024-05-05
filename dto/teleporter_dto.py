class TeleporterDto:
    def __init__(self, map_id: int, teleporters: []):
        self.map_id = map_id
        self.teleporters = teleporters

    def __repr__(self):
        return f"TeleporterDto(map_id={self.map_id}, teleporters={self.teleporters})"
