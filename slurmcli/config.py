"""Configuration for Slurm CLI"""
import json
from typing import TypeVar


T = TypeVar('T')


# TODO: store config separately for each base_url
class Config:
    """Slurm CLI COnfiguration"""
    def __init__(self, data: dict = None, fpath: str = None):
        self.data = data if data else {}
        self.fpath = fpath

    def get(self, key: str) -> T:
        """Returns the value to which the specified key is mapped

        It returns None if this map contains no mapping for the key
        """
        return self.data.get(key, None)

    def put(self, key: str, value: T):
        """Associates the specified value with the specified key in this map"""
        self.data[key] = value

        with open(self.fpath, 'w') as f:
            json.dump(self.data, f)

    @classmethod
    def from_json(cls, fpath):
        with open(fpath, 'r') as f:
            data = json.load(f)

        return cls(data=data, fpath=fpath)
