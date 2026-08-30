# Hardware Setup

Wiring guide for the sensors and actuators this code expects, on a Raspberry Pi 3 Model B.
Pin numbers below are **physical header pins** unless marked `BCM`, which is what the code
(`config.properties`, `run_greenhouse.py`, `turn_it_all_off.py`) actually addresses.

## Parts list

- Raspberry Pi 3 Model B
- AM2302 (wired DHT22) temperature/humidity sensor
- 10kΩ resistor — pull-up on the AM2302 data line (recommended by the Adafruit datasheet;
  some AM2302 modules have one built in already, check before doubling up)
- MCP3008 8-channel SPI ADC — the Pi has no analog input pins, and the soil moisture sensor
  is analog
- Capacitive soil moisture sensor (analog output)
- 2-channel relay module, opto-isolated, with inputs that trigger from 3.3V logic
- Grow light, switched via relay channel 1
- 12V pump, switched via relay channel 2
- Jumper wires / breadboard (or a perma-proto board for a permanent build)

## 1. Enable SPI

The MCP3008 is read over hardware SPI0 (`run_greenhouse.py` uses `SPI_PORT=0, SPI_DEVICE=0`),
which is off by default:

```bash
sudo raspi-config
# Interface Options -> SPI -> Enable
sudo reboot
```

## 2. Header layout (what's used)

```
              3.3V  (1) (2)  5V
   AM2302 VCC ----> (1)              MCP3008 VDD/VREF ← 3.3V, use pin 17
   MCP3008 VDD ---> (17)             Relay VCC (5V)   ← use pin 2 or 4
              5V    (3) (4)  5V
                     ...
        GPIO4/AM2302 DATA (7) (8)   BCM14
                    GND   (9) (10)  BCM15
                  BCM17  (11) (12)  BCM18
                  BCM27  (13) (14)  GND
                  BCM22  (15) (16)  BCM23  ← water_channel (relay IN2)
              3.3V (17) (18)  BCM24  ← light_channel (relay IN1)
       MOSI  BCM10 (19) (20)  GND
       MISO  BCM9  (21) (22)  BCM25
       SCLK  BCM11 (23) (24)  BCM8 (CE0)  ← MCP3008 CS/SHDN
                    GND (25) (26)  BCM7
                     ...
```

Used pins, summarized:

| Physical pin | BCM | Used for |
|---|---|---|
| 1 | — | 3.3V — AM2302 VCC |
| 6 | — | GND — AM2302 GND |
| 7 | GPIO4 | AM2302 DATA (`config.properties` → `[AM2302] pin = 4`) |
| 9 | — | GND — MCP3008 AGND/DGND |
| 16 | GPIO23 | `water_channel` → relay IN2 (pump) |
| 17 | — | 3.3V — MCP3008 VDD/VREF, soil moisture sensor VCC |
| 18 | GPIO24 | `light_channel` → relay IN1 (grow light) |
| 19 | GPIO10 (MOSI) | MCP3008 DIN |
| 21 | GPIO9 (MISO) | MCP3008 DOUT |
| 23 | GPIO11 (SCLK) | MCP3008 CLK |
| 24 | GPIO8 (CE0) | MCP3008 CS/SHDN |
| 2 or 4 | — | 5V — relay module VCC |

## 3. AM2302 (greenhouse temp/humidity)

```
AM2302 VCC  -> Pi Pin 1  (3.3V)
AM2302 GND  -> Pi Pin 6  (GND)
AM2302 DATA -> Pi Pin 7  (BCM4)
```

Add the 10kΩ resistor between VCC and DATA on the sensor side. If you move the sensor to a
different pin, update `pin` under `[AM2302]` in `config.properties` to match the new BCM number.

## 4. MCP3008 ADC + soil moisture sensor

The ADC exists because `run_greenhouse.py` reads all 8 channels every cycle for "water level"
(soil moisture), currently only channel 0 is used — channels 1–7 are free for the light sensor
etc. mentioned in the README's Plans section.

```
MCP3008 VDD      -> Pi Pin 17 (3.3V)
MCP3008 VREF     -> Pi Pin 17 (3.3V)
MCP3008 AGND     -> Pi Pin 9  (GND)
MCP3008 DGND     -> Pi Pin 9  (GND)
MCP3008 CLK      -> Pi Pin 23 (BCM11 / SCLK)
MCP3008 DOUT     -> Pi Pin 21 (BCM9  / MISO)
MCP3008 DIN      -> Pi Pin 19 (BCM10 / MOSI)
MCP3008 CS/SHDN  -> Pi Pin 24 (BCM8  / CE0)

Soil moisture sensor VCC  -> 3.3V (Pi Pin 1 or 17)
Soil moisture sensor GND  -> GND
Soil moisture sensor AOUT -> MCP3008 CH0
```

`mcp.read_adc(0)` in `run_greenhouse.py` is what reads this channel.

## 5. Light relay (grow light)

```
Pi Pin 18 (BCM24, light_channel) -> Relay IN1
Pi GND                            -> Relay GND
Pi Pin 2 or 4 (5V)                -> Relay VCC
```

Relay channel 1's COM/NO contacts go in series with the grow light's live/positive feed from
its own power source — **do not power the light itself from the Pi**, the relay only switches it.

## 6. Water pump relay

```
Pi Pin 16 (BCM23, water_channel) -> Relay IN2
```

Same relay module, channel 2. COM/NO contacts go in series with the pump's positive feed from a
12V supply.

> The code currently only ever turns this pin **off** (on startup in `turn_it_all_off.py`, and
> on exit in `run_greenhouse.py`'s signal handler) — wire it up now, but there's no logic yet
> that switches it on based on soil moisture.

## 7. Powering it all off-grid (car battery + solar)

Not built or tested yet — the code above assumes a normal 5V USB supply to the Pi for now — but
the wiring this doc describes is what a battery/solar setup would hang off:

- A 12V→5V buck converter (rated for the Pi 3B's ~2.5A peak) to run the Pi itself from the
  battery, in place of the USB adapter.
- The grow light and pump relays wired to the 12V battery line directly (as above), not to the
  Pi's own 5V rail — the Pi's GPIO/5V pins can't supply pump/light current.
- Most relay modules already include a flyback diode across the relay coil, needed since the
  pump is an inductive load — check your module's datasheet before assuming so.

## Verifying

```bash
# AM2302 sanity check (from README)
cd Adafruit_Python_DHT/examples
sudo ./AdafruitDHT.py 2302 4

# MCP3008 + relay wiring: run the control loop and watch the printed water level change
# as you cover/uncover the soil moisture sensor
python run_greenhouse.py
```
