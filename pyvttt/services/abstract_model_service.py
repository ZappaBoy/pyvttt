from abc import ABC, abstractmethod

from pyvttt.models.device import Device
from pyvttt.shared.utils.logger import Logger


class AbstractModelService(ABC):
    device: Device = Device.GPU

    def __init__(self, force_cpu: bool = False):
        self.logger = Logger()
        if force_cpu:
            self.set_device(Device.CPU)
        else:
            self.set_device(self.get_available_device())
        self.logger.info(f"Using device: {self.device}")

    @abstractmethod
    def set_threads(self, threads: int) -> None:
        pass

    def set_device(self, device: Device) -> None:
        self.device = device

    @abstractmethod
    def get_available_device(self) -> Device:
        pass

    def is_gpu_available(self):
        return self.device == Device.GPU
