from gpiozero import CPUTemperature


class CPU:
    """
    Represents CPU as a data source
    """
    def __init__(self):
        self.cpu = CPUTemperature

    def read(self):
        return self.cpu.temperature