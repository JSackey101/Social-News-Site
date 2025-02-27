""" Contains functions to handle the read/write operations. """

import os
import json

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

def save_to_file(data: list[dict]) -> None:
    """ Save the data to a file called stories.json. """
    with open(os.path.join(ABS_PATH, data), mode="w", encoding="UTF-8") as f:
        json.dump(data, f, indent=3)


def load_from_file() -> list[dict]:
    """ Load the stories from a file called stories.json. """
    with open(os.path.join(ABS_PATH, "stories.json"), encoding="UTF-8") as file:
        data = json.load(file)
        return data
