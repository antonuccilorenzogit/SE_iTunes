from dataclasses import dataclass


@dataclass
class Album():
    id: int
    title: str
    artist_id: int
    durata: int

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f'[{self.id}] {self.title} ({self.artist_id})'

    def __eq__(self, other):
        return self.id == other.id