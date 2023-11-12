import re

# Define regular expressions for common response patterns
PATTERN_ALL = re.compile(r".* in(\d+) all")
PATTERN_OUT = re.compile(r".* in(\d+) out(\d+)")

# Define configuration for matrix devices
MatrixDevices = {
    "4KMX42-H2A": {
        "inputCount": 4,
        "outputCount": 2,
        "audioOutputs": [
            "hdmiaudioout1",
            "hdmiaudioout2",
            "audioout1",
            "spdifaudioout2",
        ],
        "EDIDParamCount": 11,
        "maxDelayInMin": 30,
        "irModeCount": 2,
        "commandCount": 24,
    }
}
