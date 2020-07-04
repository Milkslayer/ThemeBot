import json
from pathlib import Path


def make_dir(dir_path):
    Path(dir_path).mkdir()


def file_exists(file_path: str) -> bool:
    if Path(file_path).exists():
        return True
    return False


def save_file_json(file_name: str, content):
    mode = "w+"
    file_name += ".json"
    with open(file_name, mode) as outfile:
        json.dump(content, outfile)


def read_file_json(file_name: str):
    file_name += ".json"
    with open(file_name) as outfile:
        if outfile.read(1):
            outfile.seek(0)
            return json.load(outfile)
        else:
            return 0