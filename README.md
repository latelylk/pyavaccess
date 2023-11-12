# pyavaccess

Python libary for interfacing with AV Access devices over serial. Designed for use with [Home Assistant](http://home-assistant.io).

## Supported Devices

* [Av Access 4×2 4K HDMI Matrix (4kmx42-h2a)](https://www.avaccess.com/products/4kmx42-h2a/)

Although this library was created for and tested with the 4kmx42-h2a, it was written so that it could be easily expanded for use with any AV Access device.

### Have a different device?

If you're a developer - please consider contributing to this project :)

If you're not a developer - open an issue with the model and features of your device and I'll see what I can do

## Usage

```python
from pyavaccess import HDMIMatrixSerial

# Interface with a "4kmx42-h2a" device over serial at "/dev/ttyUSB0"
av = HDMIMatrixSerial("/dev/ttyUSB0", "4KMX42-H2A")

# Print current version
print(av.getVer())

# Get a map of active input for each output {out: in, ...}
outputMap = av.getMappings()

# For each output, print the input mapped to it
for output, input in outputMap.items():
    print("Output {} is mapped to input {}".format(output, input))

# Set the input for output 1 to input 4
av.mapOutput(1, 4)

# Check that the mapping was successful
assert av.getMapping(1)[1] == 4
```
