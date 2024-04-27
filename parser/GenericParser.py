import asyncio
import concurrent.futures
from typing import List, Dict, Callable, Union
import os
from pathlib import Path
import itertools
from typing import List, Dict, Callable, Union
import logging
from concurrent.futures import ThreadPoolExecutor

class GenericParser:
    def __init__(self, file_address: str, end_pattern: str, first_index: int,
                 action_list: Dict[str, Callable[[Dict[str, List[List[str]]]], object]],
                 logger: logging.Logger, log_language: object):
        self.file_address = file_address
        self.end_pattern = end_pattern
        self.first_index = first_index
        self.action_list = action_list
        self.logger = logger
        self.log_language = log_language
        self.type_accessor = None

    async def get_dtos_async(self, splitter: str = "\t") -> List[object]:
        items = self.parse_text_from_file()
        result_collection = []

        with ThreadPoolExecutor() as executor:
            tasks = [executor.submit(self.process_item, item, splitter) for item in items]
            for task in asyncio.as_completed(tasks):
                result_collection.extend(await task)

        return result_collection

    def parse_text_from_file(self) -> List[str]:
        with open(self.file_address, 'r', encoding='utf-8') as file:
            content = file.read()
            items = content.split(self.end_pattern)
            return [f"{'' if idx == 0 else self.end_pattern}{item}" for idx, item in enumerate(items)]

    async def process_item(self, item: str, splitter: str) -> List[object]:
        lines = [line.split(splitter) for line in item.splitlines() if line.strip()]
        lines = {line[self.first_index][0]: line for line in lines if len(line) > self.first_index}

        result_collection = []
        for _ in range(len(lines)):
            parsed_item = {}
            try:
                for action_on_key in self.action_list:
                    parsed_item[action_on_key] = self.action_list[action_on_key](lines)
            except Exception as ex:
                self.logger.error(f"Error while parsing item: {item}", exc_info=ex)
            else:
                result_collection.append(parsed_item)

        return result_collection
