"""Track results and output to CSV file"""

import csv
from typing import List


class GameResult:
    def __init__(self, game_id: int, groups_identified: int, total_attempts: int):
        self.game_id = game_id
        self.groups_identified = groups_identified
        self.total_attempts = total_attempts


class ResultsTracker:
    def __init__(self, file_name_prefix: str):
        self.file_name_prefix = file_name_prefix

    def save_result(self, result: GameResult):
        """Save result as CSV file"""
        file_name = self.__get_file_name(result.game_id)
        with open(file_name, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter="\t")
            writer.writerow(["Groups Identified", "Total Attempts"])
            writer.writerow([result.groups_identified, result.total_attempts])

    def already_has_result(self, game_id: int) -> bool:
        """Determine if result has already been saved"""
        file_name = self.__get_file_name(game_id)
        try:
            with open(file_name, "r") as csvfile:
                return True
        except FileNotFoundError:
            return False

    def __get_file_name(self, game_id: int) -> str:
        return f"output/{self.file_name_prefix}/{game_id}.csv"
