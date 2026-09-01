import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3008 import MCP3008


class Mcp3008Adc:
    """
    Adapter over the Blinka/CircuitPython MCP3008 driver, exposing the read_adc(channel) ->
    int [0, 1023] interface the rest of this codebase (SoilMoistureDataSource, run_greenhouse.py)
    expects
    """
    def __init__(self):
        spi = busio.SPI(clock=board.SCLK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.CE0)
        self._mcp = MCP3008(spi, cs)

    def read_adc(self, channel):
        return self._mcp.read(channel)
