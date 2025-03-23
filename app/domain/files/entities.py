from dataclasses import dataclass


@dataclass
class StoredFile:
    filename: str
    data: bytes