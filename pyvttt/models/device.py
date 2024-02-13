from enum import Enum


class Device(str, Enum):
    CPU = 'CPU',
    GPU = 'GPU',

    def __str__(self):
        return self.value
