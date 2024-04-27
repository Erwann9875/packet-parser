import codecs
from typing import Dict, List, Callable

class GenericParser:
    def __init__(self, file_address: str, end_pattern: str, first_index: int,
                 action_list: Dict[str, Callable[[Dict[str, List[List[str]]]], object]]):
        self.file_address = file_address
        self.end_pattern = end_pattern
        self.first_index = first_index
        self.action_list = action_list

    def parse_text_from_file(self) -> List[str]:
        with codecs.open(self.file_address, 'r', encoding='windows-1252') as file:
            content = file.read()
            items = content.split(self.end_pattern)
            return [f"{'' if idx == 0 else self.end_pattern}{item}" for idx, item in enumerate(items)]

    def process_item(self, item: str, splitter: str) -> List[object]:
        lines = [line.split(splitter) for line in item.splitlines() if line.strip()]
        lines = {line[self.first_index][0]: line for line in lines if len(line) > self.first_index}

        result_collection = []
        for _ in range(len(lines)):
            parsed_item = {}
            try:
                for action_on_key in self.action_list:
                    parsed_item[action_on_key] = self.action_list[action_on_key](lines)
            except Exception as ex:
                print(f"Error while parsing item: {ex}")
            else:
                result_collection.append(parsed_item)

        return result_collection

    def get_dtos(self, splitter: str = "\t") -> List[object]:
        items = self.parse_text_from_file()
        result_collection = []

        for item in items:
            result_collection.extend(self.process_item(item, splitter))

        return result_collection
